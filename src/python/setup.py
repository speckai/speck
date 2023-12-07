from setuptools import find_packages, setup


def readme():
    with open("../../README.md") as f:
        README = f.read()
    return README


def parse_requirements(filename):
    with open(filename, "r") as f:
        requirements = f.read().splitlines()
    return requirements


install_requires = [
    "annotated-types==0.6.0",
    "anyio==3.7.1",
    "certifi==2023.7.22",
    "charset-normalizer==3.3.2",
    "distro==1.8.0",
    "h11==0.14.0",
    "httpcore==1.0.2",
    "httpx==0.25.1",
    "idna==3.4",
    "openai==1.2.4",
    "pydantic==2.5.0",
    "pydantic_core==2.14.1",
    "replicate==0.21.0",
    "requests==2.31.0",
    "sniffio==1.3.0",
    "tqdm==4.66.1",
    "typing_extensions==4.8.0",
    "urllib3==2.1.0",
]


setup(
    name="speck",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="0.0.3",
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
    download_url="https://github.com/speckai/speck/archive/refs/tags/v0.0.3.tar.gz",
    author="Lucas Jaggernauth",
    author_email="luke@speck.chat",
    classifiers=[
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    install_requires=install_requires,
)
