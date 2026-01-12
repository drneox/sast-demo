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
# Production mode (debug disabled)
python app.py

# Development mode with debug enabled
FLASK_DEBUG=true python app.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

- **View Users**: Homepage displays all users in the database
- **Add User**: Click "Add New User" button and fill out the form
- **Delete User**: Click "Delete" button next to any user
- **Search Users**: Use the search box to find users by name or email

## Configuration

The application supports the following environment variables:

- `SECRET_KEY`: Flask secret key for session management (defaults to a development key)
- `FLASK_DEBUG`: Enable debug mode (`true` or `false`, defaults to `false`)

## Security

The project includes a CodeQL SAST workflow (`.github/workflows/codeql.yml`) that:
- Runs on push/pull requests to main/master branches
- Uses security-extended queries for comprehensive analysis
- Automatically scans Python code for security vulnerabilities

### Testing CodeQL Detection

This repository includes a test branch (`copilot/introduce-sql-injection-vulnerability`) that demonstrates CodeQL's ability to detect SQL injection vulnerabilities:

- **Test Branch**: Contains an intentional SQL injection vulnerability in the search feature
- **Purpose**: Validate CodeQL's static analysis capabilities
- **Documentation**: See `SQL_INJECTION_TEST.md` for detailed vulnerability analysis
- **Expected Result**: CodeQL should flag the vulnerability when scanning the test branch

**⚠️ WARNING**: The test branch contains intentional security vulnerabilities and should NOT be merged into main/master.