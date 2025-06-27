from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="Anime-Recommendation-System",
    version="0.1.0",
    author="Joe",
    description="A simple anime recommendation system using collaborative filtering.",
    packages=find_packages(),
    install_requires=requirements,
)