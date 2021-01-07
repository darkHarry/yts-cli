import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="yts",
    version="1.0.0",
    description="A CLI to download yts movies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darkHarry/yts-cli",
    author="Harry S. Mecwan",
    author_email="harry.mecwan91@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="yts cli movies-downloader",
    packages=setuptools.find_packages(include=["yts"]),
    install_requires=[
        'beautifulsoup4==4.8.2',
        'bs4==0.0.1',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'idna==2.9',
        'lxml==4.6.2',
        'requests==2.23.0',
        'soupsieve==2.0',
        'urllib3==1.25.8',
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "yts=yts.yts:main"
        ]
    }
)
