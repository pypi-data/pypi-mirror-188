from setuptools import setup, find_packages
import json
import os

with open(os.path.join("config", "config.json"), "r") as f:
    data = json.load(f)

setup(
    name=data['name'],
    packages=find_packages(exclude=['network', 'hardware', 'preprocessing', 'reader']),
    version=data['Version'],
    license=data["License"],
    long_description=data["Description"],
    description="Simple and Useful Deep Learning Framework..",
    author=data["Author"],
    author_email=data["Mail"],
    url=data['url'],
    download_url=data["Download-Url"],
    python_requires=data['python_requires'],
    classifiers=data['classifiers'],
    install_requires=data['Install-Requires']
)
