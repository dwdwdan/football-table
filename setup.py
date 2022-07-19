from setuptools import setup, find_packages
import os.path as path

long_desc = open(path.join(path.dirname(__file__), "README.md")).read()

setup(
    name="football-table",
    version="0.0.1",
    author="Dan Walters",
    author_email="dan.walters5@outlook.com",
    description="A CLI to do football tables",
    url="https://github.com/dwdwdan/football-table",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
                "football-table=football_table.cli:main",
            ]
        },
    long_description=long_desc,
    long_description_content_type="text/markdown",
)
