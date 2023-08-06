import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("Octrapy/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

setuptools.setup(
    name="Octra.py",
    description="An async API wrapper for Octra bot API in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Akash",
    url="https://github.com/Octra/Octra.py",
    project_urls={
        "Documentation": "https://Octrapy.readthedocs.io",
        "Issue tracker": "https://github.com/Octra/Octra.py/issues",
    },
    version=version,
    packages=["Octrapy", "Octrapy/ext/commands"],
    install_requires=requirements,
    extras_require={
        "docs": [
            "sphinx==2.4.3",
            "sphinx-rtd-theme",
            "sphinxcontrib_trio==1.1.1",
            "sphinxcontrib-websupport",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
