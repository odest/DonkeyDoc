<p align="center">
<img src="https://raw.githubusercontent.com/odest/DonkeyDoc/master/docs/logo.png" alt="logo" width="80" height="80"/>
</p>

<br>

<div align="center">

DonkeyDoc
===========================
<h4> A cross-platform fluent Doc Viewer </h4>

[![release](https://github.com/odest/DonkeyDoc/actions/workflows/release.yml/badge.svg)](https://github.com/odest/DonkeyDoc/actions/workflows/release.yml)
[![python](https://img.shields.io/badge/python-3.12.0-green)](https://www.python.org/downloads/release/python-3120/)
[![pyqt5](https://img.shields.io/badge/PyQt5-5.15.10-green)](https://pypi.org/project/PyQt5/5.15.10/)
[![tag](https://img.shields.io/badge/tag-v1.0.0-green)](https://github.com/odest/DonkeyDoc/releases/tag/v1.0.0)
[![license](https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820)](https://github.com/odest/DonkeyDoc?tab=GPL-3.0-1-ov-file)
[![Platform Win32 | Linux | macOS](https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820)]()
---

<br>

<div align="center">

**DonkeyDoc** is an open-source, cross-platform document viewer designed for a seamless and intuitive user experience. Built with a focus on fluidity and performance, **DonkeyDoc** aims to provide users with a reliable tool for viewing and reading various types of documents.

</div></div>



<center>

![banner](https://raw.githubusercontent.com/odest/DonkeyDoc/master/docs/banner.png)

</center>

<br>

> [!NOTE]
> Running v1.0.0 release on **Windows 11** with **Mica Effect** and **Dark/Light** Mode

<br>

## Table of Contents

  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Screenshots](#screenshots)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Getting the Code](#getting-the-code)
    - [Downloading the Code](#downloading-the-code)
    - [Cloning with Git](#cloning-with-git)
    - [Installing the Package](#installing-the-package)
    - [Running the Program](#running-the-program)
  - [Story Behind the Project Name](#story-behind-the-project-name)
  - [License](#license)

<br>

## Features

**DonkeyDoc** offers a comprehensive set of features designed to enhance your document viewing experience. Here are some of the key features:

- **Supports Multiple File Formats**: **DonkeyDoc** can open the following various file types:
  - **Image Formats**: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`, `.svg`
  - **Document Formats**: `.pdf`, `.epub`, `.txt`, `.mobi`, `.xps`, `.fb2`, `.cbz`

  <br>
  <details>
    <summary>Details</summary>

    #### Image Formats
    - **PNG**: Portable Network Graphics (PNG) is a raster graphics file format that supports lossless data compression.<br>
    - **JPG**: Joint Photographic Experts Group (JPG) is a commonly used method of lossy compression for digital images.<br>
    - **JPEG**: Joint Photographic Experts Group (JPEG) is another name for JPG, used for compressing digital images.<br>
    - **BMP**: Bitmap (BMP) is an image file format used for storing bitmap digital images.<br>
    - **TIFF**: Tagged Image File Format (TIFF) is a format for high-quality images and is often used in scanning.<br>
    - **SVG**: Scalable Vector Graphics (SVG) is an XML-based format for vector graphics that can be scaled to any size.<br>

  #### Document Formats
    - **PDF**: Portable Document Format (PDF) is a versatile file format commonly used for documents.<br>
    - **EPUB**: Electronic Publication (EPUB) is a popular format for eBooks and digital publications.<br>
    - **TXT**: Plain Text (TXT) is a simple text file format with no formatting or special features.<br>
    - **MOBI**: Mobipocket (MOBI) is an eBook format used primarily for Amazon Kindle devices.<br>
    - **XPS**: XML Paper Specification (XPS) is a format similar to PDF used for document sharing.<br>
    - **FB2**: FictionBook (FB2) is an XML-based eBook format commonly used for fiction books.<br>
    - **CBZ**: Comic Book Zip (CBZ) is a file format used for comic book archives.<br>
  </details>

- **Decryption Support**: If a file is encrypted, **DonkeyDoc** decrypts files by asking you for a password to decrypt the document.

- **Tab Management**: Open and manage multiple documents simultaneously using the tab feature. You can switch between tabs and swipe them around for added convenience.

- **Enhanced Document Navigation**: After opening a file, you can access a Table of Contents menu on the left side and a text/HTML content display menu on the right side for easier navigation and reading.

- **Versatile Toolbar**: The toolbar offers the following functions:
  - Navigating forward and backward through pages
  - Jumping to a specific page
  - Rotating pages
  - Zooming in and out
  - Fitting pages to screen or resizing them as needed
  - Displaying file information and metadata
  - Switching between dark and light modes effortlessly

- **Customizable Settings**: Tailor the application to your preferences with the following configuration options:
  - **Mica Effect**: Enable or disable the Mica effect (Windows 11 only)
  - **Theme Selection**: Choose and customize the program’s theme and color scheme
  - **Interface Zoom**: Adjust the zoom level of the interface to suit your needs

With these features, **DonkeyDoc** is designed to be a powerful, flexible, and user-friendly document viewer that adapts to your preferences and workflow.


<br>

## Screenshots

> [!IMPORTANT]
> - Mica effect is only enable for Windows 11
> - Aero effect is not available in this version but will be added as an option in future releases

Running v1.0.0 release on **Windows 11** with **Mica Effect**   |  Running next release Demo on **Windows 11** with **Aero Effect**
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/odest/DonkeyDoc/master/docs/win11.png)  |  ![](https://raw.githubusercontent.com/odest/DonkeyDoc/master/docs/demo.png)


<br>

## Installation

To download **DonkeyDoc**, visit the [**Releases**](https://github.com/odest/DonkeyDoc/releases) section of the **GitHub** repository and download the latest release for your system under the "Assets" section.

**DonkeyDoc** is available for **Windows**, **macOS** _(Apple Silicon & Intel)_, and **Linux**.

Windows and Linux builds are also available in **portable** versions if you want a more self-contained executable to move around.

> [!IMPORTANT]
> Not tested on macOS but, you may be met with a message saying _""**DonkeyDoc**" can't be opened because Apple cannot check it for malicious software."_ If you encounter this, then you'll need to go to the "Settings" app, navigate to "Privacy & Security", and scroll down to a section that says _""**DonkeyDoc**" was blocked from use because it is not from an identified developer."_ Click the "Open Anyway" button to allow **DonkeyDoc** to run. You should only have to do this once after downloading the application.

<br>

## Usage

After downloading the file suitable for your operating system, extract it from the ZIP archive and run the program.

When the program opens, you will need to select the file or files you wish to view. You can do this in one of the following ways:

- **Drag and Drop**: Simply drag the files into the application window.
- **File Picker**: Use the built-in file picker to browse and select your files.
- **Paste File**: Copy the file and paste it directly into the application.

Once the files are selected, they will be checked for compatibility. If the files are supported, they will be opened and displayed for you to view.

> [!NOTE]
> For more detailed information and a step-by-step guide, a video tutorial will be added in the future.


<br>



## Getting the Code

To obtain a local copy of the project, follow these steps:

### Downloading the Code

1. **Download the ZIP File**: You can download the code as a ZIP file from the following link:
   - **[Download Source Code](https://github.com/odest/DonkeyDoc/archive/refs/heads/master.zip)**

   Alternatively, you can download the latest release directly from the **GitHub Releases** page by navigating to the **[Releases](https://github.com/odest/DonkeyDoc/releases)** section and downloading the **ZIP** file under **Assets**.

2. **Extract the ZIP File**: Unzip the downloaded file to a location of your choice.

3. **Navigate to the Project Directory**: Go to the directory where you extracted the ZIP file.

### Cloning with Git

Alternatively, you can clone the repository using **Git**:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/odest/DonkeyDoc.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd DonkeyDoc
   ```

### Installing the Package

Once you have the code, install the package and its dependencies using `pip`:

```bash
pip install .
```

By following these steps, you will have successfully installed and run **DonkeyDoc**.

### Running the Program

To run the project, open a terminal in the project directory and execute the following command based on your operating system:

- **Windows**:
  ```bash
  python main.py
  ```

- **Linux/macOS**:
  ```bash
  python3 main.py
  ```

This will start the application.


<br>


## Story Behind the Project Name

<img align="right" width="320" height="192" src="https://raw.githubusercontent.com/odest/DonkeyDoc/master/docs/souvenir.gif">

The reason I chose this name is rooted in a childhood memory from the farm where I grew up.

When I was young, I had just finished my homework and left it unattended for a moment. When I came back, our donkey had eaten almost all of it. There was nothing I could do—the homework was gone, and I didn’t have time to redo it. When I went to school and my teacher asked about the homework, I explained that the donkey had eaten it. My teacher scolded me, saying she thought I was making excuses, and the whole class laughed at me. I still remember it vividly.

When I was brainstorming names for this project, this memory suddenly came back to me. I thought there couldn’t be a better name than this one, as it carries a personal story, is memorable, and even adds a touch of humor. This is why I decided on **DonkeyDoc** for my project.

<br>

## License  
- *This project is licensed under the* **GPL-3.0 License** - *see the* [LICENSE](https://github.com/odest/DonkeyDoc?tab=GPL-3.0-1-ov-file) *file for details.*
