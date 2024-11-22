from setuptools import setup, find_packages

setup(
    name="switchbot-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "switchbot=src.main:cli",
        ],
    },
)
