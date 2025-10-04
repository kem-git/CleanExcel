# CleanExcel - Automated Data Cleaner

**Version:** 1.0  
**Platform:** Windows (GUI)

---

## Overview

CleanExcel is a modern, easy-to-use **Excel and CSV data cleaning tool** with a GUI. It allows you to automatically clean your datasets, remove duplicates, handle missing values, trim text columns, and standardize column names — all without writing a single line of code.

With CleanExcel, you can:

- **Load Excel (.xlsx) or CSV files**  
- **Automatically detect headers**  
- **Preview your data in a table**  
- **Clean your data** using customizable options  
- **Save cleaned data** back to Excel or CSV  

---

## Features

1. **Automatic Header Detection**  
   - Detects whether the file has headers or generates default column names.  

2. **Duplicate Removal**  
   - Removes duplicate rows intelligently, ignoring whitespace and case.  

3. **Missing Value Handling**  
   - Fills numeric columns with median values and text columns with blanks.  

4. **Text Trimming**  
   - Automatically trims whitespace from text columns.  

5. **Column Standardization**  
   - Converts column names to lowercase and replaces spaces with underscores.  

6. **Preview Table**  
   - See the first 50 rows of your cleaned data before saving.  

7. **Modern GUI**  
   - Translucent, intuitive interface with buttons for loading, cleaning, previewing, and saving.

---

## How to Use

1. **Launch the App**  
   - Double-click `CleanExcel.exe` (Windows) or run `python app.py` (Python environment).  

2. **Load Your File**  
   - Click `Load File` and select an Excel or CSV file.  

3. **Select Cleaning Options**  
   - Choose which cleaning steps to apply:
     - Remove Duplicates
     - Fill Missing Values
     - Trim Text Columns
     - Standardize Column Names  

4. **Clean Data**  
   - Click `Clean Data` to process the dataset.  

5. **Preview Cleaned Data**  
   - Click `Preview Cleaned Data` to see the first 50 rows.  

6. **Save Cleaned Data**  
   - Click `Save Cleaned File` to save your dataset in Excel or CSV format.

---

## Installation (Python Version)

1. Install dependencies:

```bash
pip install pandas openpyxl
```

2. Run the file:

```bash
python app.py
```
