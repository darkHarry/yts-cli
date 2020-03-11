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
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "yts=yts.yts:main"
        ]
    }
)
