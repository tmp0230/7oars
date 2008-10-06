import jobs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = 'pyjobs',
    version = jobs.__version__,
    description = 'Extras for pyprocessing to manage processes.',
    long_description = jobs.__doc__,
    author = jobs.__author__,
    author_email = 'john -at- 7oars.com',
    url = 'http://code.google.com/p/7oars/',
    download_url = 'http://code.google.com/p/7oars/downloads/list',
    license = 'BSD',
    platforms = ['POSIX', 'Windows'],
    keywords = ['pyprocessing', 'processing', 'threading', 'distributed', 'multiprocessing'],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],
    packages = ['jobs'],
    test_suite = 'jobs.tests.suite',
    install_requires=['processing'],
    zip_safe=True,
)