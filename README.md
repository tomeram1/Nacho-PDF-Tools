# Nacho PDF Tools 📄🛠️

A lightweight, standalone Windows desktop application for managing PDF files. Designed for simplicity and speed, this tool allows users to effortlessly merge multiple PDFs, reorder them, or extract specific pages using a clean graphical user interface.

## ✨ Key Features

* **Merge PDFs:** Select multiple PDF files, arrange them in your desired order using the built-in UI, and merge them into a single document.
* **Split & Extract:** Select a specific PDF and extract individual pages or page ranges (e.g., `1-3, 5, 8-10`).
* **OS Integration:** Seamlessly integrates into the Windows "Send To" context menu. Simply select your PDFs, right-click, and send them directly to the app.
* **Standalone Executable:** Compiled into a single, dependency-free `.exe` file. End-users do not need to install Python or any external libraries to use the software.
* **Add on the Fly:** Forgot a file? Use the built-in "Add" button to browse and append more PDFs directly from the UI.

## 💻 Tech Stack

* **Language:** Python 3
* **GUI Framework:** Tkinter (Native Windows Look & Feel)
* **PDF Processing:** PyPDF2
* **Compilation:** Nuitka (Translates Python to C and compiles to machine code for maximum performance and security)
* **Automation:** Windows Batch / PowerShell (For seamless installation and registry/shortcut management)

## 🚀 Getting Started

### For Regular Users (Installation)
1. Navigate to the **Releases** tab on the right side of this repository.
2. Download the latest `PDF_Tools_Setup.zip` file.
3. Extract the ZIP file to any folder.
4. Run `Install.bat`. 
5. **Usage:** Highlight one or more PDF files, right-click -> **Send to** -> **PDF Tools**.

### For Developers (Running from Source)
If you want to explore or modify the code:

1. Clone the repository:
   ```bash
   git clone [https://github.com/tomeram1/Nacho-PDF-Tools.git](https://github.com/tomeram1/Nacho-PDF-Tools.git)
