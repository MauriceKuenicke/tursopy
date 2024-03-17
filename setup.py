from setuptools import find_packages, setup

setup(
    name="tursopy",
    version="0.0.1",
    packages=find_packages(),
    author="Maurice Künicke",
    description="Fully type-hinted Turso Platform API wrapper for Python.",
    long_description="Fully type-hinted Turso Platform API wrapper for Python.",
    url="https://github.com/MauriceKuenicke/tursopy",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)
