from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests>=2"]

setup(
    name="smsman",
    version="1.0.3",
    author="Dmitry Tikhomirov",
    author_email="dimasta00@gmail.com",
    description="A package to simplify work with the sms-man API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/smsmancom/smsman/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requiers=">3.6"
)
