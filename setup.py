from pathlib import Path

from setuptools import setup, find_packages

README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="bmgo-wrapper",
    version="3.31.1.0",
    author="quefep-bmgo",
    description=(
        "Unofficial Python API wrapper for Blockman GO with login, profiles, "
        "leaderboards, friends, groups, and RongCloud group chat."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=("LICENSE",),
    url="https://github.com/quefep-bmgo/bmgo-wrapper",
    project_urls={
        "Documentation": "https://github.com/quefep-bmgo/bmgo-wrapper#readme",
        "Group chat guide": "https://github.com/quefep-bmgo/bmgo-wrapper/blob/main/docs/group-chat.md",
        "Source": "https://github.com/quefep-bmgo/bmgo-wrapper",
        "Issues": "https://github.com/quefep-bmgo/bmgo-wrapper/issues",
    },
    keywords=[
        "blockman go",
        "blockman go api",
        "blockman go api wrapper",
        "blockman go python",
        "blockman go bot",
        "blockmango",
        "bmgo",
        "bmgo-wrapper",
        "api wrapper",
        "rongcloud",
        "game api",
        "python",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28",
        "httpx>=0.24",
        "pycryptodome>=3.19",
        "python-dotenv>=1.0",
        "websocket-client>=1.6",
    ],
)
