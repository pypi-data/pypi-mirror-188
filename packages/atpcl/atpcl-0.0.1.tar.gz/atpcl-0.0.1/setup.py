from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name="atpcl",
    version="0.0.1",
    url="https://github.com/mirceamesesan/atpcl-tracker",
    description="Time tracking made easy",
    author=[{
        "name":"Mircea Mesesan",
        "email": "mircea@atpcl.one"
        }],
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['atpcl'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "License :: Freeware",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        ],
    install_requires = [
        "pandas >= 1.2",
        "requests >= 2.0",
        ],
)