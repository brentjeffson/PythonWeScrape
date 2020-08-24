from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text()

setup(
    name="WeScrape",
    version="0.1",
    description="Collection of anime, novel, manga, and youtube parsers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brent Jeffson F. Florendo",
    author_email="brentjeffson@gmail.com",
    license="MIT",
    python_requires='~=3.7',
    package=find_packages(exclude=(
        "tests", ".vscode", "wescrape/run.py",
    )),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4==4.9.1',
        'lxml==4.5.2'
    ]
)