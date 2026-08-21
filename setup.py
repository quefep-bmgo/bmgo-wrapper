from setuptools import setup, find_packages

setup(
    name="bmgo-wrapper",
    version="8202026.1",
    description="Blockman GO (v3.25.1) API wrapper with full x-sign authentication",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28",
        "httpx>=0.24",
        "pycryptodome>=3.19",
    ],
)