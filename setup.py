from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['pydantic', 'Faker']

setup(
    name="models_manager",
    version="0.0.2",
    author="Nikita Filonov",
    author_email="filonov.nikitkaa@gmail.com",
    description="Models Manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikita-Filonov/models_manager",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
