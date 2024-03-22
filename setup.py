from setuptools import find_packages, setup

setup(
    name="az_completion_fns",
    version="0.0.1",
    packages=find_packages(include=["az_completion_fns", "az_completion_fns.*"]),
)
