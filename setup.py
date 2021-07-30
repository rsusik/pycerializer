import io
from setuptools import setup, find_packages
from pycerializer import __version__

setup(
    name="pycerializer",
    version=__version__,
    author="Robert Susik",
    author_email="robert.susik@gmail.com",
    options={"bdist_wheel": {"universal": True}},    
    license="GPLv3",
    description=(
        """This module performs conversions between Python values 
        (numbers and dictionaries) and C structs represented 
        as Python bytes objects."""
    ),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    entry_points={},
    package_data={},
    package_dir={"": "."},
    packages=find_packages(where="."),
    url="https://github.com/rsusik/pycerializer",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5", # Because of `typing`
        "Topic :: Software Development",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: Utilities",
    ],
)