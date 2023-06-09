from setuptools import Extension

from typing import Optional, List

class ZigExtension(Extension):
    def __init__(
        self,
        name: str,
        sources: List[str],
        include_dirs: Optional[List[str]]=None,
        define_macros: Optional[List[str]]=None,
        undef_macros: Optional[List[str]]=None,
        library_dirs: Optional[List[str]]=None,
        libraries: Optional[List[str]]=None,
        runtime_library_dirs: Optional[List[str]]=None,
        extra_objects: Optional[List[str]]=None,
        extra_c_compile_args: Optional[List[str]]=None,
        extra_zig_compile_args: Optional[List[str]]=None,
        extra_link_args: Optional[List[str]]=None,
        export_symbols: Optional[List[str]]=None,
        swig_opts: Optional[List[str]]=None,
        depends: Optional[List[str]]=None,
        language: Optional[str]=None,
        optional: Optional[bool]=None,
        **kw  # To catch unknown keywords. Not used.
        ) -> None:
        
        Extension.__init__(
            self=self,
            name=name,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            undef_macros=undef_macros,
            library_dirs=library_dirs,
            libraries=libraries,
            runtime_library_dirs=runtime_library_dirs,
            extra_objects=extra_objects,
            extra_compile_args=extra_c_compile_args,
            extra_link_args=extra_link_args,
            export_symbols=export_symbols,
            swig_opts=swig_opts,
            depends=depends,
            language=language,
            optional=optional,
            kw
        )

        self.extra_zig_compile_args = extra_zig_compile_args 

