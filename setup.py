import setuptools
from modular_conf import __version__


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setuptools.setup(
    name='modular-conf',
    version=__version__,
    scripts=[],
    author='Michael Loipfuehrer',
    author_email='',
    description='A modular python configuration utility',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='http://github.com/mikonse/modular_conf',
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[

    ],
)
