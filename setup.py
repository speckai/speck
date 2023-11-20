from setuptools import setup


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


setup(
    name="python-speck",
    version="0.0.0",
    description="Speck - Unified observability platform for production LLM apps",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/speckai/speck",
    author="Lucas Jaggernauth",
    author_email="luke@speck.chat",
    classifiers=[
        "Programming Language :: Python :: 3.12",
    ],
    packages=["py-automl"],
    include_package_data=True,
    install_requires=[],
)
