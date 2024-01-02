from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


def parse_requirements(filename):
    with open(filename, "r") as f:
        requirements = f.read().splitlines()
    return requirements


install_requires = [
    "openai",
    "replicate",
    "requests",
    "pydantic",
]


setup(
    name="speck",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="0.0.8",
    description="Speck - The dev framework for LLM apps.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=[
        "speck",
        "openai",
        "llm",
        "ai",
        "chat",
        "bot",
        "gpt",
        "gpt-3",
        "gpt-4",
        "anthropic",
        "replicate",
    ],
    url="https://github.com/speckai/speck",
    download_url="https://github.com/speckai/speck/archive/refs/tags/v0.0.8.tar.gz",
    homepage="https://speck.chat",
    author="",
    author_email="Lucas Jaggernauth <luke@speck.chat>, Raghav Pillai <raghav@speck.chat>",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=install_requires,
)
