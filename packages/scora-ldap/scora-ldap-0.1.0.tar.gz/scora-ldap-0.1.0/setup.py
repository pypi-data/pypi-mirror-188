from setuptools import setup, find_packages
from pkgver import package_version
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


install_reqs = ["ldap3>=2.9.1", "boto3>=1.26.57", "numpy>=1.24.1"]

setup(
    name="scora-ldap",
    version=package_version,
    description="Scora Ldap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={"scora_ldap/pkgver": "pkgver"},
    install_requires=install_reqs,
    python_requires=">=3.8",
    zip_safe=True,
    author="Oncase",
    author_email="contato@oncase.com.br",
    maintainer="Guilherme Morone",
    maintainer_email="guilherme.morone@oncase.com.br",
    url="https://github.com/oncase/scora-ldap",
    license="MIT",
    keywords="scora",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
)
