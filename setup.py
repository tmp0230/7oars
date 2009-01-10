import stopwatch

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = 'stopwatch',
    version = stopwatch.__version__,
    description = 'stopwatch is a very simple python module for measuring time.',
    long_description = stopwatch.__doc__,
    author = stopwatch.__author__,
    author_email = 'john -at- 7oars.com',
    url = 'http://code.google.com/p/7oars/',
    download_url = 'http://code.google.com/p/7oars/downloads/list',
    license = 'BSD',
    platforms = ['POSIX', 'Windows'],
    keywords = ['timer', 'watch', 'execution', 'timeit'],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],
    packages = ['stopwatch'],
    test_suite = 'stopwatch.tests.suite',
    zip_safe=True,
)
