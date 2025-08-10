
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
	<a href="https://cs50.harvard.edu/certificates/your-certificate-link">
		<img src="https://img.shields.io/badge/CS50P-Certificate-01a4f1" alt="CS50P Certificate">
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
3. [🖥️ How It Looks: GUI, CLI & Documents](#-how-it-looks-gui-cli--documents)
4. [🧪 Tests & Datasets Preview](#-tests--datasets-preview)
5. [📦 PyPI & Documentation Links](#-pypi--documentation-links)
6. [💾 Standalone App Details](#-standalone-app-details)
7. [📚 Notes & References](#-notes--references)

---

## 📋 Project Overview

**CS50P Final Project** | MSP Tech Club, Misr International University


Attendance data gathering for technical sessions at Misr International University, including MSP Tech Club, was time-consuming and error-prone. This tool automates the process by:


- Accepting Google Forms CSV exports as input
- Validating and normalizing data (course code, time, university ID, etc.)
- Exporting formatted Word/PDF documents as required by the university
- Handling edge cases and missing data with clear validation logs
- Providing both CLI and GUI interfaces for flexibility
- Designed for both developers (as a PyPI package, subsystem for MSP's website/system) and non-developers (standalone setup wizard)
- Heavily tested with `pytest` and multiple sample datasets
- Fully documented on [ReadTheDocs](https://attendance-automation-msp.readthedocs.io/)

---

## 📄 CSV Format Requirements


Your CSV file **must** contain the following columns (headers), named exactly as shown:

- Full Name
- University ID
- Course Code
- Course Time
- Doctor/TA Name

These columns are required for successful processing. If any are missing or empty, the tool will raise an error and the file will not be processed.

> Columns like `Timestamp` and `Email` are *not required*. The tool does not expect or require a timestamp column. The `University Email` column is only validated if present, but is not mandatory.


---


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

![GUI Preview](https://github.com/user-attachments/assets/672f0692-5520-4827-bbd0-28f9bb56b0d4)

### Exported Document Preview
Shows a sample exported document with normalized/validated data and a log for any missing or incorrect fields.

![Exported Document Preview](https://github.com/user-attachments/assets/dd84b1fc-9e30-4921-ac88-1beb43c35c33)

### CLI Preview
Flexible command-line automation for exporting, formatting, and validating attendance data.

![CLI Preview](https://github.com/user-attachments/assets/203bcd66-c7f5-4724-ba24-01192f928757)

## 🧪 Tests & Datasets Preview

Extensive edge case testing using `pytest`:

- Automated tests for all major features
- Validation of correct and incorrect data
- Sample tests in [`tests/`](tests/)
- Sample datasets for testing in [`datasets/`](datasets/)
- Usage guides in [`tests/USAGE.md`](tests/USAGE.md) and [`datasets/USAGE.md`](datasets/USAGE.md)

### Test Suite Preview

This will automatically discover and run all sample and edge case tests, providing a summary of results.

![Test Suite Preview](https://github.com/user-attachments/assets/7064447d-d558-401a-a9ea-24b07a82c6d4)

---

## 📦 PyPI & Documentation Links

- **PyPI Package:** [attendance-tool-msp](https://pypi.org/project/attendance-tool-msp/)
- **Documentation:** [ReadTheDocs](https://attendance-tool-msp.readthedocs.io/en/latest/)
- **CS50P Certificate:** [View Certificate](https://cs50.harvard.edu/certificates/your-certificate-link)

---

## 💾 Standalone App Details


For non-developers, a professional setup wizard is available:

- Download: [AttendanceToolMSP_1.0.3_setup.exe](https://raw.githubusercontent.com/mohamedelziat50/attendance-automation-MSP/distributing-installer/installer/AttendanceToolMSP_1.0.3_setup.exe)

- Only the **Word** export functionality is distributed in the standalone app for simplicity and reliability.

    ![Setup Wizard Preview](https://github.com/user-attachments/assets/21c10e7b-953c-480a-94f3-80b405ef44ba)

- **Note:** When you run the installer, Windows may show a "Windows protected your PC" warning. This happens because the installer was created by me and I do not yet have a trusted certificate authority to sign the app (Publisher: Unknown Publisher). This is common for new or independent software developers.

	<img width="450" alt="Image" src="https://github.com/user-attachments/assets/c64d49f3-9150-4254-9cc7-82874b59b029" />

- To proceed, click **More info** and then **Run anyway**. Rest assured, the app is safe to use and will not harm your computer.


---

## 📚 Notes & References

- **CS50P Handwritten Notes:** [`Handwritten Notes.pdf`](notes/CS50P%20-%20Handwritten%20Notes.pdf)
- **Packaging (UV, PyPI, Setup Wizard):** [`Packaging - UV & PyPi & Setup Wizard.docx`](notes/Packaging%20-%20UV%20&%20PyPi%20&%20Setup%20Wizard.docx)
- **Documentation (Sphinx, ReadTheDocs):** [`Documenting - Sphinx & Read The Docs.docx`](notes/Documenting%20-%20Sphinx%20&%20Read%20The%20Docs.docx)

---

<div align="center">
	<sub>Made with ❤️ for MSP Tech Club & Misr International University</sub>
</div>
