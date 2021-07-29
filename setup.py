import io
from setuptools import setup, find_packages
from binpacker import __version__

# def get_requirements():
#     with open("requirements.txt") as fp:
#         return [req for req in (line.strip() for line in fp) if req and not req.startswith("#")]

setup(
    name="binpacker",
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
    #install_requires=get_requirements(),
    python_requires=">=3.0",
    entry_points={},
    #package_dir={"": "."},
    # packages = [
    #     'binpacker'
    # ],
    package_data={},
    #url="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: Utilities",
    ],
)