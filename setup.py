from setuptools import setup
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirements = []
if os.path.isfile("./requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    requirements = [x for x in requirements.split("\n") if x != ""]

setup(
    name="ma5_expert",
    version="1.0.5",
    description=("MadAnalysis 5 interpreter for Expert mode"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MadAnalysis/ma5_expert",
    project_urls={
        "Bug Tracker": "https://github.com/MadAnalysis/ma5_expert/issues",
    },
    download_url = "https://github.com/MadAnalysis/ma5_expert/archive/refs/tags/v1.0.4.tar.gz",
    author="Jack Y. Araz",
    author_email=("jack.araz@durham.ac.uk"),
    license="MIT",
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)
