# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:28:33 2025

@author: adamp
"""

"""
Installation script for Project_Flow
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="project_flow",
    version="0.1.0",
    author="Project_Flow Contributors",
    author_email="admin@project-flow.org",
    description="A comprehensive user interface for OpenFOAM CFD simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamRNP/Project_Flow",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "project_flow=project_flow.main:main",
        ],
    },
    include_package_data=True,
)
