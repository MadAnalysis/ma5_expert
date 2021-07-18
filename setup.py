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
    version="0.0.1",
    description=("MadAnalysis 5 interpreter for Expert mode"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackaraz/ma5_expert",
    author="Jack Y. Araz",
    author_email=("jack.araz@durham.ac.uk"),
    license="MIT",
    packages=[
        "ma5_expert",
        "ma5_expert.CutFlow",
        "ma5_expert.tools",
    ],
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