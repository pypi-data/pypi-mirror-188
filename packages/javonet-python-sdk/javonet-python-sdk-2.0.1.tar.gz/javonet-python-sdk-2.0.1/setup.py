import setuptools

setuptools.setup(
    name="javonet-python-sdk",
    version="2.0.1",
    author="SdNcenter Sp. z o.o.",
    author_email="support@javonet.com",
    description="Javonet SDK for Python",
    url="https://javonet.com",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
