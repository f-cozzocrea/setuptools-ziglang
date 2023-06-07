from setuptools.errors import SetupError
from setuptools.command.build_ext import build_ext

import sys

class build_zig_ext(build_ext):
    def build_extension(self, ext):
        self.compiler.set_executable("compiler", ["zig", "cc"])
        self.compiler.set_executable("compiler_so", ["zig", "cc"])
        self.compiler.set_executable("compiler_cxx", ["zig", "cc"])
        self.compiler.set_executable("linker_so", ["zig", "cc", "-shared"])
        self.compiler.set_executable("linker_exe", ["zig", "cc"])
        self.compiler.set_executable("archiver", ["zig", "ar", "-cr"])
        
        sources = ext.sources
        if sources is None or not isinstance(sources, (list, tuple)):
            raise SetupError(
                "in 'ext_modules' option (extension '%s'), "
                "'sources' must be present and must be "
                "a list of source filenames" % ext.name
            )
        # sort to make the resulting .so file build reproducible
        sources = sorted(sources)

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

        # Next, compile the source code to object files.

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




