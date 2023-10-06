import subprocess
from pathlib import Path

from setuptools import find_packages, setup

__author__ = "arv-anshul"
__author_email__ = "arv.anshul.1864@gmail.com"
__author_github__ = "https://github.com/arv-anshul/"
__project_repo__ = "https://github.com/arv-anshul/easy-analysis"

readme_path = Path("README.md")
requirements_path = Path("requirements.txt")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Copied from https://github.com/cfengine/cf-remote/blob/master/setup.py
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
package_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in package_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v, i, s = package_version.split("-")
    package_version = v + "+" + i + ".git." + s

assert "-" not in package_version
assert "." in package_version
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #

setup(
    name="arv-easy_analysis",
    version=package_version,
    description="Data Analysis makes easy.",
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    url=__project_repo__,
    license="MIT",
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    include_package_data=True,
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
