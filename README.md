
# 📝 Attendance Automation Tool - MSP

<div align="center">
    <br>
	<img src="https://raw.githubusercontent.com/mohamedelziat50/attendance-automation-MSP/main/images/MSP_Logo_Transparent.png" alt="MSP Logo" width="300" style="display: block;"/>
    <br><br>
	<a href="https://pypi.org/project/attendance-tool-msp/">
		<img src="https://img.shields.io/badge/PyPI-v1.0.3-01a4f1" alt="PyPI">
	</a>
	<a href="https://attendance-automation-msp.readthedocs.io/">
		<img src="https://img.shields.io/badge/ReadTheDocs-online-f25123" alt="ReadTheDocs">
	</a>
	<a href="https://docs.google.com/forms/d/19Yr79Zj9nwbu76-deXBJqYttGGCyzbok7AIZX19zFtM/template/preview">
    <img src="https://img.shields.io/badge/Google%20Forms-Template-01a4f1" alt="Google Forms Template">
	</a>
	<a href="https://cs50.harvard.edu/certificates/36cfc1ad-7e8f-4be1-bfa2-2cdda3db14e0">
		<img src="https://img.shields.io/badge/CS50P-Certificate-f25123" alt="CS50P Certificate">
	</a>
</a>
	<br>
	<a href="#-standalone-app-details">
		<img src="https://img.shields.io/badge/Download%20Standalone%20App-AttendanceToolMSP_1.0.3_setup-7fba00" alt="Download Standalone App">
	</a>
</div>

---

## 📑 Table of Contents

1. [📋 Project Overview](#-project-overview)
2. [📄 CSV Format Requirements](#-csv-format-requirements)
3. [🖥️ How It Looks: GUI, CLI & Documents](#how-it-looks-preview)
4. [🧪 Tests & Datasets Preview](#-tests--datasets-preview)
5. [📦 Quick Access Links](#-quick-access-links)
6. [💾 Standalone App Details](#-standalone-app-details)
7. [🛠️ Local Package Development](#local-package-development)
8. [🤝 Open Source & Contributions](#-open-source--contributions)
9. [📚 Notes & References](#-notes--references)

---

## 📋 Project Overview

**CS50P Final Project** | MSP Tech Club, Misr International University


Attendance data gathering for technical sessions at Misr International University, including MSP Tech Club, was time-consuming and error-prone. This tool automates the process by:


- Accepting Google Forms CSV exports as input (see [CSV Format Requirements](#-csv-format-requirements) below; works with any CSV file containing the required headers; a [Google Forms Template is available here](https://docs.google.com/forms/d/19Yr79Zj9nwbu76-deXBJqYttGGCyzbok7AIZX19zFtM/template/preview))
- Validating and normalizing data (course code, time, university ID, etc.)
- Exporting formatted Word/PDF documents as required by the university
	- *Note: If you need page numbers in exported Word documents, add them manually in Word: Insert → Page Number → Bottom of Page → Plain Number 2 (centered). This is due to a python-docx limitation.*
- Handling edge cases and missing data with clear validation logs
- Providing both CLI and GUI interfaces for flexibility (see [How It Looks: GUI, CLI & Documents](#how-it-looks-preview) below)
- Designed for both developers (as a [PyPI package](https://pypi.org/project/attendance-tool-msp/), subsystem for MSP's website/system) and non-developers (standalone setup wizard; see [Standalone App Details](#-standalone-app-details) below)
- Heavily tested with `pytest` and multiple sample datasets (see [Tests & Datasets Preview](#-tests--datasets-preview) below)
- Fully documented on [ReadTheDocs](https://attendance-automation-msp.readthedocs.io/)
- Tested on Windows natively and on Ubuntu Linux (using [Oracle VirtualBox](https://www.virtualbox.org/) for virtualization).  
  See screenshots: [Ubuntu Package Tested](images/Ubuntu%20Package%20Tested.jpg) & [Ubuntu Standalone Tested](images/Ubuntu%20Standalone%20Tested.jpg)

---

## 📄 CSV Format Requirements

> Need a quick start? Use our [Google Forms Template](https://docs.google.com/forms/d/19Yr79Zj9nwbu76-deXBJqYttGGCyzbok7AIZX19zFtM/template/preview) to generate compatible CSV files.

Your CSV file **must** contain the following columns (headers), named exactly as shown:

- Full Name
- University ID
- Course Code
- Course Time
- Doctor/TA Name

These columns are required for successful processing. If any are missing or empty, the tool will raise an error and the file will not be processed.

> Columns like `Timestamp` and `Email` are *not required*. The tool does not expect or require a timestamp column. The `University Email` column is only validated if present, but is not mandatory.


---

<a id="how-it-looks-preview"></a>
## 🖥️ How It Looks: GUI, CLI & Documents

> The following commands are intended for local development of this package after cloning this repository. For package usage, please refer to the [PyPI package page](https://pypi.org/project/attendance-tool-msp/). These commands are not required when using the standalone app (just double-click the app to run it).

Run via command line for quick development:

```bash
python main.py                                               # GUI mode
python main.py <file.csv> --word --title <title>             # Export mode
python main.py <file.csv> --pdf --title <title>              # Export mode
```


### GUI Preview
Modern, user-friendly interface for selecting attendance sheets and export options.

![GUI Preview](https://github.com/user-attachments/assets/2550dd5b-df63-431f-9593-d76053a10ecd)

### Exported Document Preview
Shows a sample exported document with normalized/validated data and a log for any missing or incorrect fields.

![Exported Document Preview](https://github.com/user-attachments/assets/b0ea7ac4-bdf3-437e-9051-a874ccf122da)

### CLI Preview
Flexible command-line automation for exporting, formatting, and validating attendance data.

![CLI Preview](https://github.com/user-attachments/assets/c7337f85-5fe9-4524-925c-41122c452c0d)

## 🧪 Tests & Datasets Preview

Extensive edge case testing using `pytest`:

- Automated tests for all major features
- Validation of correct and incorrect data
- Sample tests in [`tests/`](tests/)
- Sample datasets for testing in [`datasets/`](datasets/)
- Usage guides in [`tests/USAGE.md`](tests/USAGE.md) and [`datasets/USAGE.md`](datasets/USAGE.md)

### Test Suite Preview

This will automatically discover and run all sample and edge case tests, providing a summary of results.

![Test Suite Preview](https://github.com/user-attachments/assets/d4a87fc4-248a-4f4e-9ce7-0b46a8c5f447)

---

## 📦 Quick Access Links

- **PyPI Package:** [attendance-tool-msp](https://pypi.org/project/attendance-tool-msp/)
- **Documentation:** [ReadTheDocs](https://attendance-automation-msp.readthedocs.io/)
- **Google Forms Template:** [Access Template](https://docs.google.com/forms/d/19Yr79Zj9nwbu76-deXBJqYttGGCyzbok7AIZX19zFtM/template/preview)
- **CS50P Certificate:** [View Certificate](https://cs50.harvard.edu/certificates/36cfc1ad-7e8f-4be1-bfa2-2cdda3db14e0)
 - **CS50P Final Project Video:** [CS50P Final Project Video - Attendance Automation Tool MSP](https://youtu.be/f-6z_AavnPo)

---

## 💾 Standalone App Details

> The standalone app is designed for non-developers who want a simple, professional setup experience. It is distributed as a Windows installer and can also be run on Ubuntu Linux using Wine. Please read the instructions below for your operating system.

For non-developers, a professional setup wizard is available:

- Download: [AttendanceToolMSP_1.0.3_setup.exe](https://raw.githubusercontent.com/mohamedelziat50/attendance-automation-MSP/distributing-installer/installer/AttendanceToolMSP_1.0.3_setup.exe)

- Only the **Word** export functionality is distributed in the standalone app for simplicity and reliability.

### 💻 Windows 

> The standalone app requires administrator privileges to export files (e.g., saving Word documents). This is a standard requirement for file operations in some Windows environments. Rest assured, the app is safe and only requests these permissions to save your exported documents securely.

![Setup Wizard Preview](https://github.com/user-attachments/assets/0a436620-5b05-4cc4-8dd9-9cdc47c45b31)

**Note:** When you run the installer, Windows may show a "Windows protected your PC" warning. This happens because the installer was created by me and I do not yet have a trusted certificate authority to sign the app (Publisher: Unknown Publisher). This is common for new or independent software developers.

<img width="450" alt="Image" src="https://github.com/user-attachments/assets/c64d49f3-9150-4254-9cc7-82874b59b029" />

To proceed, click **More info** and then **Run anyway**. Rest assured, the app is safe to use and will not harm your computer.

### 🐧 Linux/Ubuntu

> The standalone app can also be run on Linux systems using **[Wine](https://www.winehq.org/)**, a free and open-source compatibility layer that allows Windows applications to run on Unix-like operating systems without a full Windows installation.

**1. Install Wine (if not already installed):**
```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine64 wine32
```

You can check Wine’s version after install:
```bash
wine --version
```

**2. Configure Wine (first run):**
```bash
winecfg
```
This will create Wine’s configuration folder, you can leave most settings as default.  


**3. Run Your .exe Setup File:**
Navigate to your `.exe` location:
```bash
cd /path/to/your/file
wine AttendanceToolMSP_1.0.3_setup.exe
```
This should launch the Windows installer inside Ubuntu.

> **Tested on Windows natively and on Ubuntu (using [Oracle VirtualBox](https://www.virtualbox.org/) for virtualization).**  
> See screenshots: [Ubuntu Package Tested](images/Ubuntu%20Package%20Tested.jpg) & [Ubuntu Standalone Tested](images/Ubuntu%20Standalone%20Tested.jpg)

---

<a id="local-package-development"></a>
## 🛠️ Local Package Development 

This project uses [uv](https://github.com/astral-sh/uv) for fast, modern Python dependency management: making setup simple and reproducible for open source development.


### To set up your environment after cloning (from the project root):

**1. Install uv (if not already installed):**
```bash
pip install uv
```

**2. Create a virtual environment:**
```bash
uv venv
```

**3. Activate the virtual environment:**
```bash
.venv\Scripts\activate
```

**4. Install dependencies from `pyproject.toml`:**
```bash
uv pip install -r attendance_tool_msp/pyproject.toml
```

**5. Verify dependencies are installed:**
```bash
uv pip list
```

> This installs the dependencies (using `-r` flag: "requirements") listed in `pyproject.toml` inside your virtual environment, so you can add features, fix bugs, and run tests easily. Files are designed for local development of the package in this repository.


In VS Code, also select the `.venv` interpreter from the bottom right corner to ensure your terminal and IDE use the same environment:

<img width="710" height="151" alt="Image" src="https://github.com/user-attachments/assets/1b5d6b2b-91f1-4a7a-bf34-dc703af6a631" />

---

## 🤝 Open Source & Contributions

This project is open-source and welcomes community involvement! You can:
- Open issues for bugs or feature requests
- Fork the repository and submit pull requests (PRs) for new features or fixes
- Help improve documentation and usability

Every contribution makes the project better for everyone. Thank you for the support!

## 📚 Notes & References

- **CS50P Handwritten Notes:** [`Handwritten Notes.pdf`](notes/CS50P%20-%20Handwritten%20Notes.pdf)
- **Packaging (UV, PyPI, Setup Wizard):** [`Packaging - UV & PyPi & Setup Wizard.docx`](notes/Packaging%20-%20UV%20&%20PyPi%20&%20Setup%20Wizard.docx)
- **Documentation (Sphinx, ReadTheDocs):** [`Documenting - Sphinx & Read The Docs.docx`](notes/Documenting%20-%20Sphinx%20&%20Read%20The%20Docs.docx)

---

<div align="center">
	<sub>Made with ❤️ for MSP Tech Club & Misr International University</sub>
</div>
