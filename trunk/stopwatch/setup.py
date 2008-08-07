import stopwatch

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = "stopwatch",
    version = stopwatch.__version__,
    description = "Python easily measuring execution time.",
    long_description = stopwatch.__doc__,
    author = "John Paulett",
    author_email = "john@7oars.com",
    url = "http://code.google.com/p/7oars/",
    license = "BSD",
    platforms = ['POSIX', 'Windows'],
    keywords = ['timer', 'watch', 'execution'],
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers"
    ],
    options = { 'clean' : { 'all' : 1 } },
    packages = ["stopwatch"],
    #test_suite = 'stopwatch.tests.suite',
    zip_safe=True,
)