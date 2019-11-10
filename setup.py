import io
import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(
    os.path.join(here, "codechain", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

requires = [
    "rlp",
    "coincurve",
    "dataclasses; python_version < '3.7'",
    "pycrypto",
    "jsondatabase",
]

setup(
    name=about["__title__"],
    version=about["__version__"],
    url=about["__url__"],
    project_urls={
        "Documentation": "",
        "Code": "https://github.com/CodeChain-io/codechain-sdk-python",
        "Issue tracker": "https://github.com/CodeChain-io/codechain-sdk-python/issues",
    },
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=readme,
    packages=find_packages(),
    license=about["__license__"],
    install_requires=requires,
    extras_require={"dev": ["pytest"]},
    python_requires=">=3.6",
)
