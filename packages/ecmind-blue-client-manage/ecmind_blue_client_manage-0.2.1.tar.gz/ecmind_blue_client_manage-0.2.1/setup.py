import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecmind_blue_client_manage",
    version="0.2.1",
    author="Roland Koller, Ulrich Wohlfeil & other contributers",
    author_email="info@ecmind.ch",
    description="Helper modules for the `ecmind_blue_client` to ease the work with management APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ecmind.ch/open/ecmind_blue_client_manage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["ecmind_blue_client>=0.4.6", "XmlElement>=0.3.1", "ftfy"],
    extras_require={},
)
