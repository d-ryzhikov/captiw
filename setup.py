from setuptools import find_packages, setup

LICENSE_CLASSIFIER = "License :: OSI Approved :: MIT License"

setup(
    name="captiw",
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
