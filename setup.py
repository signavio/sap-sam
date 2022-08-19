from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="sapsam",
    packages=['sapsam'],
    package_dir={'':'src'},
    version="0.0.1",
    description="long description",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
