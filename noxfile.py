import nox

python_versions = ["3.7", "3.8", "3.9", "3.10", "3.11",] ## "pypy3.8", "pypy3.9"]

@nox.session(python=python_versions)
def test_c(session):
    session.install(".")
    session.install("build")

    with session.chdir("testing/c_sum"):
       session.run(session.python, '-m', 'build')
       session.run()


@nox.session(python=python_versions)
def test_zig(session):
    session.install("build")

    with session.chdir("testing/zig_sum"):


    session.install("pytest")

