import sys

import setuptools

try:
    with open("README.md", "r") as fin:
        long_description = fin.read()
except:
    long_description = "A library to make parallel selenium tests that automatically download webdriver\n"

try:
    with open("requirements.txt", "r") as reqs:
        requirements = reqs.read().split("\n")
except:
    requirements = ""

try:
    if "refs/tags/v" in sys.argv[1]:
        versionName = sys.argv[1].replace("refs/tags/v", "")
        del sys.argv[1]
    else:
        raise Exception
except:
    versionName = "0.1.0"

setuptools.setup(
    name="autoparaselenium",
    version=versionName,
    author="Ronak Badhe",
    author_email="ronak.badhe@gmail.com",
    description=long_description.split("\n")[1],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r2dev2/AutoParaSelenium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
