from setuptools import Extension
from setuptools._distutils.errors import DistutilsSetupError
from setuptools._distutils.dep_util import newer_group 
from setuptools.command.build_ext import build_ext

import sys
import logging as log

log.basicConfig(level=log.INFO)


class ZigExtension(Extension):
    pass 


class build_zig_ext(build_ext):
    def build_extension(self, ext):

        # Use regular build_ext method for non-ZigExtensions
        if not isinstance(ext, ZigExtension):
            build_ext.build_extension(ext)
            return

        self.compiler.set_executable("compiler", ["zig", "cc"])
        self.compiler.set_executable("compiler_so", ["zig", "cc"])
        self.compiler.set_executable("compiler_cxx", ["zig", "cc"])
        self.compiler.set_executable("linker_so", ["zig", "cc", "-shared"])
        self.compiler.set_executable("linker_exe", ["zig", "cc"])
        self.compiler.set_executable("archiver", ["zig", "ar", "-cr"])
        
        sources = ext.sources
        if sources is None or not isinstance(sources, (list, tuple)):
            raise DistutilsSetupError(
                "in 'ext_modules' option (extension '%s'), "
                "'sources' must be present and must be "
                "a list of source filenames" % ext.name
            )

        ext_path = self.get_ext_fullpath(ext.name)
        depends = sources + ext.depends
        if not (self.force or newer_group(depends, ext_path, 'newer')):
            log.debug("skipping '%s' extension (up-to-date)", ext.name)
            return
        else:
            log.info("building '%s' extension", ext.name)

        # First, scan the sources for SWIG definition files (.i), run
        # SWIG on 'em to create .c files, and modify the sources list
        # accordingly.
        sources = self.swig_sources(sources, ext)

        # sort to make the resulting .so file build reproducible
        zig_sources = []
        c_sources = []
        for f in sources:
            if f.endswith('.zig'):
                zig_sources.append(f)
            else:
                c_sources.append(f)
        
        sources = sorted(sources)
        zig_sources = sorted(zig_sources)
        c_sources = sorted(c_sources)

        ### This code is copied from zaml. Need to update and modify for this lib.
        if not os.path.exists(self.build_lib):
            os.makedirs(self.build_lib)
        windows = platform.system() == "Windows"
        self.spawn(
            [
                "zig",
                "build-lib",
                "-O",
                "ReleaseFast",
                "-lc",
                *(["-target", "x86_64-windows-msvc"] if windows else []),
                f"-femit-bin={self.get_ext_fullpath(ext.name)}",
                "-fallow-shlib-undefined",
                "-dynamic",
                *[f"-I{d}" for d in self.include_dirs],
                *(
                    [
                        f"-L{sysconfig.get_config_var('installed_base')}\\Libs",
                        "-lpython3",
                    ]
                    if windows
                    else []
                ),
                ext.sources[0],
            ]
        )

        # Next, compile the C source code to object files.

        # XXX not honouring 'define_macros' or 'undef_macros' -- the
        # CCompiler API needs to change to accommodate this, and I
        # want to do one thing at a time!

        # Two possible sources for extra compiler arguments:
        #   - 'extra_compile_args' in Extension object
        #   - CFLAGS environment variable (not particularly
        #     elegant, but people seem to expect it and I
        #     guess it's useful)
        # The environment variable should take precedence, and
        # any sensible compiler will give precedence to later
        # command line args.  Hence we combine them in order:
        extra_args = ext.extra_compile_args or []

        macros = ext.define_macros[:]
        for undef in ext.undef_macros:
            macros.append((undef,))

        ### FIXME!!! This part and afterwards is where C code is compiled.
        ### This should happen AFTER the zig code is compiled, since the zig code may
        ### emit a C header file that this step depends on.
        objects = self.compiler.compile(
            sources,
            output_dir=self.build_temp,
            macros=macros,
            include_dirs=ext.include_dirs,
            debug=self.debug,
            extra_postargs=extra_args,
            depends=ext.depends,
        )

        # XXX outdated variable, kept here in case third-part code
        # needs it.
        self._built_objects = objects[:]

         # Now link the object files together into a "shared object" --
        # of course, first we have to figure out all the other things
        # that go into the mix.
        if ext.extra_objects:
            objects.extend(ext.extra_objects)
        extra_args = ext.extra_link_args or []

        # Detect target language, if not provided
        language = ext.language or self.compiler.detect_language(sources)

        ### FIXME!!! This is where the C code is linked to a shared object
        self.compiler.link_shared_object(
            objects,
            ext_path,
            libraries=self.get_libraries(ext),
            library_dirs=ext.library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extra_args,
            export_symbols=self.get_export_symbols(ext),
            debug=self.debug,
            build_temp=self.build_temp,
            target_lang=language,
        )




