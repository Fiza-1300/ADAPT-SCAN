"""Setup for ADAPT-SCAN project."""

from setuptools import setup, find_packages

setup(
    name="adapt-scan",
    version="0.1.0",
    description="Adaptive scanning system for SIH26055",
    author="Team SIH26055",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "gymnasium>=0.28.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
)
