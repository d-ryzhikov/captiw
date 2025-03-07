from setuptools import find_packages, setup

LICENSE_CLASSIFIER = "License :: OSI Approved :: MIT License"

with open("VERSION", "r") as f:
    version = f.read().strip()

setup(
    install_requires=[],
    name="captiw",
    version=version,
    packages=find_packages(exclude=["tests"]),
    author="Dmitry Ryzhikov",
    author_email="d.ryzhykau@gmail.com",
    license=LICENSE_CLASSIFIER,
    classifiers=[
        LICENSE_CLASSIFIER,
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Embedded Systems",
    ],
)
