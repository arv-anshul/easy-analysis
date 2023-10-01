from pathlib import Path

from setuptools import find_packages, setup

__author__ = "arv-anshul"
__author_email__ = "arv.anshul.1864@gmail.com"
__author_github__ = "https://github.com/arv-anshul/"
__project_repo__ = "https://github.com/arv-anshul/easy-analysis"

readme_path = Path("README.md")
requirements_path = Path("requirements.txt")

setup(
    name="arv-easy_analysis",
    version="0.0.1",
    description="Data Analysis makes easy.",
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    url=__project_repo__,
    license="MIT",
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(where="easy_analysis"),
    package_dir={"": "easy_analysis"},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[i for i in requirements_path.read_text().split("\n")],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
