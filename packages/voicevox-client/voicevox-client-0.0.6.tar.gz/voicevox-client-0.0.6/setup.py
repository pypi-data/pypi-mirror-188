from setuptools import setup
import re


def get_version():
    with open("voicevox/__init__.py", "r") as f:
        return re.search(r'__version__ = "([^"]+)"', f.read()).group(1)


with open("README.md", "r") as f:
    long_description = f.read()


with open("requirements.txt", "r") as f:
    requirements = f.readlines()


setup(
    name="voicevox-client",
    description="Voicevox engine unoffical wrapper",
    version=get_version(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tuna2134",
    license="MIT",
    packages=["voicevox", "voicevox.types"],
    install_requires=requirements,
    extras_require={
        "tests": [
            "pytest",
            "pytest-asyncio"
        ]
    }
)
