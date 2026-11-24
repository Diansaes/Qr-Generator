# QR Generator

Project to generate QR codes and export them as PDF files.

## Requirements

- Python 3.9 or higher

## 1. Activate the virtual environment

In Windows PowerShell, create the environment first and then activate it:

```powershell
cd "C:\path\to\project\QR_generator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If a permissions error appears:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

Once the virtual environment is active, install the project dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Usage flow
> Before to start: Add the CSV files to the `folder_1` folder


1. Initialize 
   ```
   Scripts\Activate.ps1
   ```
2. Run the program:
   ```powershell
   python qrgenerate_PDF.py
   ```
3. The script detects the CSV files in `folder_1`
4. For each CSV file, it creates a new folder with the same name as the file without the extension
5. It generates the resulting PDF files inside that folder

## 4. Deactivate the virtual environment

After finishing the task, deactivate the virtual environment with:

```powershell
deactivate
```

## Important note

Do not upload to Git:

- real CSV files
- generated PDFs
- the virtual environment
- temporary or local files
