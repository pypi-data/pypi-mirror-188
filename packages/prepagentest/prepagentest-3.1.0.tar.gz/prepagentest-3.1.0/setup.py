from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name = 'prepagentest',
    version='3.1.0',
    description='some package',
    py_modules=["ragents"],
    install_requires = [
        'pandas',
        'numpy',
        'datetime',
        'tqdm',
        'helperagent==4.0.0',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev":[
            "pytest",
        ],
    },
)