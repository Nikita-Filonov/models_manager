from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['Faker', 'psycopg2-binary']

setup(
    name="models_manager",
    version="0.7.2",
    author="Nikita Filonov",
    author_email="filonov.nikitkaa@gmail.com",
    description="Models Manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikita-Filonov/models_manager",
    packages=find_packages(),
    install_requires=requirements,
)
