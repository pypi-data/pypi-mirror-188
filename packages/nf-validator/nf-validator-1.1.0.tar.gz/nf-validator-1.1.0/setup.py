from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nf-validator",
    version="1.1.0",
    author="Sosthène Mounsamboté",
    author_email="sosthenemounsambote14@gmail.com",
    description="A package for validating name and surname",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sosthene14/NF_validating/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "unicodedata2",
    ],
)