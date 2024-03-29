#!/usr/bin/env python3
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read_requirements(file_name):
    reqs = []
    with open(os.path.join(here, file_name)) as in_f:
        for line in in_f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('git+'):
            	pkg_name = line[line.rfind('/')+1: line.rfind('.git')]
            	line = f'{pkg_name}@ {line}'
            reqs.append(line)
    return reqs


with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()


setup(
    name='Historia',
    version='1.1.0',
    url='https://github.com/MarinaStrocchi/Historia',
    author="",
    author_email="",
    license='MIT',
    description='Stefano Historia library, with some modifications for better sampling of the non-implausible region. For documentation, refer to the original repository',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        "dev": read_requirements('requirements-dev.txt'),
    },
    include_package_data=True,
    package_data={
        '': ['*.yaml', '*.repo', '*.in', '*.json']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
