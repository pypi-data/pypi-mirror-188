from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pytohm-Yvnee",
    version="0.0.1",
    author="Aryan Svendsen",
    author_email="aryansvendsen@gmail.com",
    description="This package was made to simplify the use of Ohm's Law equations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yvnee/OhmTools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)