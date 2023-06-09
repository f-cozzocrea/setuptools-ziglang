import nox

python_versions = ["2.7", "3.7", "3.8", "3.9", "3.10", "3.11",] ## "pypy3.8", "pypy3.9"]

@nox.session(python=python_versions)
def test(session):
    session.install(".")
    session.install("build")

    with session.chdir("testing/c"):
        session.run('rm', '-rf', 'build/', 'dist/',)
        session.run(session.python, '-m', 'build')
        session.install('dist/*.whl')

    with session.chdir("testing/zig"):
        session.run('rm', '-rf', 'build/', 'dist/',)
        session.run(session.python, '-m', 'build')
        session.install('dist/*.whl')



