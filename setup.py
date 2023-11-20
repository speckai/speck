from setuptools import setup


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


setup(
    name="python-speck",
    packages=["speck"],
    version="0.0.0",
    description="Speck - Unified observability platform for production LLM apps",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=["speck", "openai", "llm", "ai", "chat", "bot", "gpt", "gpt-3"],
    url="https://github.com/speckai/speck",
    download_url="https://github.com/speckai/speck/archive/refs/tags/v0.0.0.tar.gz",
    author="Lucas Jaggernauth",
    author_email="luke@speck.chat",
    classifiers=[
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    install_requires=[],
)
