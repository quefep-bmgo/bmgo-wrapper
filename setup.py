from pathlib import Path

from setuptools import setup, find_packages

README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="bmgo-wrapper",
    version="3.29.3.1",
    description="Blockman GO v3.29.3 API wrapper with x-sign authentication",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/quefep-bmgo/bmgo-wrapper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28",
        "httpx>=0.24",
        "pycryptodome>=3.19",
        "python-dotenv>=1.0",
    ],
)
