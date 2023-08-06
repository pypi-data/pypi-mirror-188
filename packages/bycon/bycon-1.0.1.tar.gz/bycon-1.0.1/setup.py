"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="bycon",
    version="1.0.1",
    description="A Python-based environment for the Beacon v2 genomics API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/progenetix/bycon",
    author="Michael Baudis",
    author_email="contact@progenetix.org",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="genomics, Beacon",
    # package_dir={"": "bycon"},  # Optional
    packages=find_packages(where="."),  # Required
    python_requires=">=3.7, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=["base36", "humps", "isodate", "json_ref_dict", "liftover", "numpy", "progress", "pyhumps", "pymongo", "PyYAML", "ruamel.base"],  # Optional
    # extras_require={  # Optional
    #     "dev": ["check-manifest"],
    #     "test": ["coverage"],
    # },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={
    #     "config": ["*"],
    #     "lib": ["*"],
    #     "rsrc": ["*"],
    #     "schemas": ["*"]
    # },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     "console_scripts": [
    #         "sample=sample:main",
    #     ],
    # },
    # List additional URLs that are relevant to your project as a dict.
    #
    project_urls={  # Optional
        "Bug Reports": "https://github.com/progenetix/bycon/issues",
        "Source": "https://github.com/progenetix/bycon/",
    },
)