from setuptools import find_packages, setup

setup(
    name="mkdocs-no-3rd-party-plugin",
    version="0.0.1",
    description="An MkDocs plugin to remove 3rd party assets and download them locally",
    long_description="",
    keywords="mkdocs privacy",
    url="https://github.com/rany2/mkdocs-no-3rd-party-plugin",
    author="rany",
    author_email="rany2@riseup.net",
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "mkdocs>=1.4.1",
        "beautifulsoup4==4.11.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "no3rdparty = mkdocs_no_3rd_party.plugin:No3rdPartyPlugin",
        ],
    },
)
