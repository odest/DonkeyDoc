import setuptools


__version__ = "1.0.0"

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="DonkeyDoc",
    version=__version__,
    keywords="cross-platform pyqt5 pdf-viewer ebook-reade pdf-reader fluent pdf-tools doc-viewer",
    author="odest",
    author_email="destrochloridium@gmail.com",
    description="A cross-platform fluent Doc Viewer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/odest/DonkeyDoc",
    packages=setuptools.find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "pymupdf",
        "darkdetect",
        "pywin32;platform_system=='Windows'",
        "xcffib;platform_system=='Linux'",
        "pyobjc;platform_system=='Darwin'",
        "PyCocoa;platform_system=='Darwin'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source Code": "https://github.com/odest/DonkeyDoc",
        "Bug Tracker": "https://github.com/odest/DonkeyDoc/issues",
    },
)
