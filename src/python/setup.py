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
]


setup(
    name="speck",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="0.0.6",
    description="Speck - LLM observability framework.",
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
    download_url="https://github.com/speckai/speck/archive/refs/tags/v0.0.6.tar.gz",
    author="Lucas Jaggernauth",
    author_email="luke@speck.chat",
    classifiers=[
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    install_requires=install_requires,
)
