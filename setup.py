import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ialarmclient-phoenix",
    version="1.0.0",
    author="Riccardo Tempesta",
    author_email="info@riccardotempesta.com",
    description="Meiantech, iAlarm, Antifurto365, AllarmiWireless and other alarm systems support",
    long_description=long_description,
    url="https://github.com/phoenix128/python-ialarmclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
