#!/usr/bin/env python

from setuptools import setup, find_packages

pkginfo = {}
with open("snvis/_version.py") as f:
    exec(f.read(), pkginfo)

with open("README.md") as readme:
    setup(
        name="snvis",
        version=pkginfo["__version__"],
        description="Social network visualising tool",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/Callum-Irving/snvis",
        author="Callum Irving",
        author_email="callum.irving04@gmail.com",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.9",
        ],
        package_dir={"": "."},
        packages=find_packages(),
        include_package_data=True,
        install_requires=["thefuzz >= 0.19.0", "python-igraph >= 0.9.8",
                          "python-Levenshtein>=0.12.2", "cairocffi>=1.3.0", "pyvis>=0.1.9"],
        entry_points={"console_scripts": ["snvis = snvis.cli.__main__:main"]}
    )
