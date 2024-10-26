#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]


setup(
    name="anime-schedules",
    version="1.0.3",
    url="https://github.com/TheProjectsX/anime-schedules",
    description="Get Anime Schedule Information easily!",
    author="TheProjectsX",
    author_email="",
    license="MIT",
    packages=["anime_schedules"],
    package_dir={"anime_schedules": "anime_schedules"},
    install_requires=requirements,
    # Include additional files
    include_package_data=True,
    # Additional classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
