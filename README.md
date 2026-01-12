# sast-demo

A simple Flask web application with database and forms, featuring CodeQL SAST security analysis.

## Features

- User management system with CRUD operations
- SQLite database integration
- HTML forms for data input
- CodeQL security scanning with `security-extended` queries

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

- **View Users**: Homepage displays all users in the database
- **Add User**: Click "Add New User" button and fill out the form
- **Delete User**: Click "Delete" button next to any user

## Security

The project includes a CodeQL SAST workflow (`.github/workflows/codeql.yml`) that:
- Runs on push/pull requests to main/master branches
- Uses security-extended queries for comprehensive analysis
- Automatically scans Python code for security vulnerabilities