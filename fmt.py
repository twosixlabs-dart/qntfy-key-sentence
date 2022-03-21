from setuptools import find_packages, setup

NAME = "spacy-analytic"
PACKAGES = find_packages()

setup(
    name=NAME,
    install_requires=[
        "falcon>=2.0.0, <3.0.0",
        "spacy>=3.0.0, <4.0.0",
        "ceeder>=0.0.1, <1.0.0",
        "gunicorn>=20.0.0",
    ],
    packages=PACKAGES,
)
