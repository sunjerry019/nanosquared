import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanosquared",
    version="0.3.8.4",
    author="Yudong Sun",
    author_email="yudong.sun@mpq.mpg.de",
    description="Automated M-Squared Measurement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunjerry019/nanosquared",
    project_urls={
        "Bug Tracker": "https://github.com/sunjerry019/nanosquared/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: Windows",
    ],
    package_dir={"": "src"},
    packages = [ # setuptools.find_packages(where="src")
        'nanosquared', 
        'nanosquared.cameras', 
        'nanosquared.common', 
        'nanosquared.fitting', 
        'nanosquared.measurement', 
        'nanosquared.stage'
    ], 
    package_data={
        'nanosquared.cameras': ['csharp/NanoScanLibrary/bin/Release/netstandard2.0/*.dll']
    }, # https://stackoverflow.com/a/1857436/3211506
    include_package_data=True,
    python_requires=">=3.8",
    install_requires = [
        "scipy>=1.6.3",
        "numpy>=1.20.3",
        "pyserial>=3.5",
        "pandas>=1.2.4",
        "wxpython>=4.1.1",
        "comtypes==1.1.8",
        "pywin32>=228",
        "pyqt5>=5.15",
        "matplotlib>=3.4.2",
        "msl-loadlib>=0.9.0",
        "pythonnet>=2.5.2",
    ]
)