# Electricity Bill Calculator - Frappe App

## Overview
This is a Frappe-based web application that allows users to input electricity usage data, calculates the bill, saves it in a Doctype, and displays all past entries in a table.

## Features
- User-friendly web form to input electricity usage details.
- Automatic bill calculation based on usage.
- Data is saved in a custom Frappe Doctype (`Electricity Bill`).
- Displays all past entries in a table format.

## Requirements
- Python 3.10+
- Frappe Framework (version 14 or compatible)
- Bench CLI installed

## Installation

1. **Navigate to your Bench directory**:
    ```bash
    cd ~/frappe-bench
    ```

2. **Get the app from local path** (if using the provided zip):
    ```bash
    bench get-app electricity_app /path/to/electricity_app
    ```

3. **Install the app on your site**:
    ```bash
    bench --site your-site-name install-app electricity_app
    ```

4. **Start the development server**:
    ```bash
    bench start
    ```

5. **Access the Web Page**:
    - Go to: `http://localhost:8000/electricity-bill-calculator`

## File Structure
```
electricity_app/
    electricity_app/
        doctype/
            electricity_bill/
                electricity_bill.json   # Doctype definition
                electricity_bill.py      # Server-side logic
        www/
            electricity-bill-calculator/
                index.html               # Frontend HTML
                index.py                  # Backend logic
    hooks.py
    modules.txt
    patches.txt
```

## Notes
- Tested on **Frappe v14**.
- Make sure you have a running site before installing the app.
- For production setup, follow Frappe deployment best practices.

## Author
Lakshya Sahrawat