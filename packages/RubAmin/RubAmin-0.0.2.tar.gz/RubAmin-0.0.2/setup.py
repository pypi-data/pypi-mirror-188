from setuptools import setup

requirements : list = ["pycryptodome" , "pillow" , "aiohttp" , "websocket-client"]

with open("README.md", "r")as fh:
    long_description = fh.read()

setup(
    name = "RubAmin",
    version = "0.0.2",
    author = "Amin Tatality",
    description = "First uploaded project by M_AminB",
    long_description_content_type ="text/markdown",
    packages = ['RubAmin'],
    install_requires = requirements,
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)