from setuptools import setup, find_packages

setup(
    name="bmgo-wrapper",
    version="8202026.2",
    description="Blockman GO v3.28.2 API wrapper with x-sign authentication",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28",
        "httpx>=0.24",
        "pycryptodome>=3.19",
    ],
)
