from setuptools._distutils.unixccompiler import UnixCCompiler, _split_env, _split_aix, _linker_params
from setuptools._distutils.ccompiler import CCompiler, gen_lib_options

import os
import sys
import logging
from sysconfig import get_config_vars

from setuptools._distutils.errors import DistutilsExecError, CompileError, LinkError

_logger = logging.getLogger(__name__)


class ZigCompiler(UnixCCompiler):
    compiler_type = 'zig'
    
    # Prefer using the PyPI zig binary, else fall back to the system zig
    try:
        import ziglang #noqa
        zig_bin = [sys.executable, '-m', 'ziglang',]
        _logger.info("Using ziglang module for compilation.")
    except (ImportError, ModuleNotFoundError) as ziglang_error:
        _logger.info("ziglang python module not found. Attempting to use system zig...")
        zig_bin = ['zig']

    zig_bin = [sys.executable, '-m', 'ziglang',]

    executables = {
        'preprocessor': None,
        'compiler': zig_bin + ["build-obj"],  
        'compiler_so': zig_bin + ["build-obj"],
        'compiler_cxx': zig_bin + ["build-obj"],
        'linker_so': zig_bin + ["build-lib"],
        'linker_exe': zig_bin + ["build-lib"],
        'archiver': zig_bin + ["ar", "-cr"],
        'ranlib': None,
    }

    if sys.platform[:6] == "darwin":
        executables['ranlib'] = [*zig_bin, "ranlib"]

    src_extensions = [".zig", ".c", ".C", ".cc", ".s", ".S", ".cxx", ".cpp", ".m", ".mm"]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    dylib_lib_extension = ".dylib"
    xcode_stub_lib_extension = ".tbd"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"
    xcode_stub_lib_format = dylib_lib_format
    if sys.platform.startswith("cygwin") or sys.platform.startswith("win32"):
        exe_extension = ".exe"


    def compile(
        self,
        sources,
        output_dir=None,
        macros=None,
        include_dirs=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        depends=None,
        ):
        breakpoint()        
        macros, objects, extra_postargs, pp_opts, build = self._setup_compile(
            output_dir, macros, include_dirs, sources, depends, extra_postargs
        )
        #cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)

        cc_args = pp_opts
        if debug:
            cc_args[:0] = ['-g']
        if extra_preargs:
            cc_args[:0] = extra_preargs

        for obj in objects:
            try:
                src, ext = build[obj]
            except KeyError:
                continue
            self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        # Return *all* object filenames, not just the ones we just built.
        return objects

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        breakpoint()
        compiler_so = self.executables['compiler_so']
        obj_path = '-femit-bin={0}'.format(obj)
        try:
            self.spawn(compiler_so + cc_args + [src, obj_path] + extra_postargs)
        except DistutilsExecError as msg:
            raise CompileError(msg)

    def link(
        self,
        target_desc,
        objects,
        output_filename,
        output_dir=None,
        libraries=None,
        library_dirs=None,
        runtime_library_dirs=None,
        export_symbols=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None,
    ):
        objects, output_dir = self._fix_object_args(objects, output_dir)
        fixed_args = self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
        libraries, library_dirs, runtime_library_dirs = fixed_args
        breakpoint()

        lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
        if not isinstance(output_dir, (str, type(None))):
            raise TypeError("'output_dir' must be a string or None")
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)

        if self._need_link(objects, output_filename):
            output_filename = "-femit-bin={0}".format(output_filename)
            ld_args = objects + self.objects + lib_opts + [output_filename]
            if debug:
                ld_args[:0] = ['-g']
            if extra_preargs:
                ld_args[:0] = extra_preargs
            if extra_postargs:
                ld_args.extend(extra_postargs)
            self.mkpath(os.path.dirname(output_filename))
            try:
                # Select a linker based on context: linker_exe when
                # building an executable or linker_so (with shared options)
                # when building a shared library.
                building_exe = target_desc == CCompiler.EXECUTABLE
                linker = (self.linker_exe if building_exe else self.linker_so)[:]

                if target_lang == "c++" and self.compiler_cxx:
                    env, linker_ne = _split_env(linker)
                    aix, linker_na = _split_aix(linker_ne)
                    _, compiler_cxx_ne = _split_env(self.compiler_cxx)
                    _, linker_exe_ne = _split_env(self.linker_exe)

                    params = _linker_params(linker_na, linker_exe_ne)
                    linker = env + aix + compiler_cxx_ne + params

                #linker = compiler_fixup(linker, ld_args)

                self.spawn(linker + ld_args)
            except DistutilsExecError as msg:
                raise LinkError(msg)
        else:
            _logger.debug("skipping %s (up-to-date)", output_filename)

    # TODO
    #def preprocess(...):
    #    ...

    # TODO
    #def create_static_lib(...):
    #    ...

    # TODO
    #def library_dir_option(...):
    #    ...

    # TODO
    #def runtime_library_dir_option(...):
    #    ...

    # TODO
    #def library_option(...):
    #    ...
   
    # TODO
    #def find_library_file(...):
    #    ...

   
    def set_default_flags(self) -> None:
        (
            cflags,
            ccshared,
            ldshared,
            shlib_suffix,
            ar_flags,
        ) = get_config_vars(
            'CFLAGS',
            'CCSHARED',
            'LDSHARED',
            'SHLIB_SUFFIX',
            'ARFLAGS',
        )
        
        # ldshared includes the executable that was used, so we need to remove it.
        ldshared = ldshared.split()
        ldshared = ldshared[1:]
        ldshared = self.executables['linker_so'] + ldshared
        ldshared = ' '.join(ldshared)

        ar = ' '.join(self.executables['archiver'])

        if 'LDFLAGS' in os.environ:
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if 'CFLAGS' in os.environ:
            cflags = cflags + ' ' + os.environ['CFLAGS']
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if 'ARFLAGS' in os.environ:
            archiver = ar + ' ' + os.environ['ARFLAGS']
        else:
            archiver = ar + ' ' + ar_flags

        zig_bin = ' '.join(self.executables['compiler'])
        zig_compile = zig_bin + ' ' + '-cflags' + ' ' + cflags + ' ' + '--'
        ldshared = zig_bin + ' ' + '-cflags' + ' ' + ldshared + ' ' + '--'

        if sys.platform.startswith("win32"):
            zig_compile += ["-target", "x86_64-windows-msvc"]

        self.set_executables(
            compiler=zig_compile,
            compiler_so=zig_compile + ' ' + ccshared,
            linker_so=ldshared,
            archiver=archiver,
        )

        self.shared_lib_extension = shlib_suffix


