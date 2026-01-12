# SQL Injection Vulnerability Test for CodeQL

## Overview
This document describes the intentional SQL injection vulnerability introduced in this branch to test CodeQL's static analysis capabilities.

## Vulnerability Details

### Location
- **File**: `app.py`
- **Function**: `search_user()`
- **Line**: 73
- **Endpoint**: `/search`

### Vulnerable Code
```python
@app.route('/search')
def search_user():
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    
    if search_query:
        # VULNERABILITY: SQL Injection - user input directly concatenated into SQL query
        # This is intentionally vulnerable for CodeQL testing purposes
        query = "SELECT * FROM users WHERE name LIKE '%" + search_query + "%' OR email LIKE '%" + search_query + "%'"
        users = conn.execute(query).fetchall()
    else:
        users = conn.execute('SELECT * FROM users').fetchall()
    
    conn.close()
    return render_template('index.html', users=users, search_query=search_query)
```

### Why This is Vulnerable
1. **Direct String Concatenation**: User input from `request.args.get('q', '')` is directly concatenated into the SQL query
2. **No Input Sanitization**: No validation or escaping of special SQL characters
3. **No Parameterized Queries**: Unlike other endpoints in the app that use `?` placeholders, this uses string concatenation

### Comparison with Safe Code
The rest of the application uses parameterized queries correctly:

**Safe Example** (from `add_user()` function):
```python
conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
```

**Vulnerable Example** (from `search_user()` function):
```python
query = "SELECT * FROM users WHERE name LIKE '%" + search_query + "%' OR email LIKE '%" + search_query + "%'"
users = conn.execute(query).fetchall()
```

## Exploitation Scenarios

### Scenario 1: Bypass Search Filter
**Payload**: `' OR '1'='1`

**Resulting Query**:
```sql
SELECT * FROM users WHERE name LIKE '%' OR '1'='1%' OR email LIKE '%' OR '1'='1%'
```

**Impact**: Returns all users in the database regardless of search criteria

### Scenario 2: UNION-Based Data Injection
**Payload**: `' UNION SELECT 999, 'Injected User', 'hacker@evil.com' --`

**Resulting Query**:
```sql
SELECT * FROM users WHERE name LIKE '%' UNION SELECT 999, 'Injected User', 'hacker@evil.com' --%' OR email LIKE '%' UNION SELECT 999, 'Injected User', 'hacker@evil.com' --%'
```

**Impact**: Injects arbitrary data into the result set

### Scenario 3: Data Exfiltration
**Payload**: `' OR 1=1 UNION SELECT sqlite_version(), sqlite_version(), sqlite_version() --`

**Impact**: Can potentially extract database metadata and other sensitive information

## Testing the Vulnerability

### Manual Testing via Browser
1. Start the application: `python app.py`
2. Navigate to `http://127.0.0.1:5000`
3. Add some test users
4. In the search box, enter: `' OR '1'='1`
5. Click "Search"
6. **Result**: All users will be displayed, bypassing the search filter

### Automated Testing
Run the test script to verify the vulnerability:
```bash
python /tmp/test_sql_injection.py
```

Expected output shows successful SQL injection attacks.

## CodeQL Detection

### Expected CodeQL Findings
CodeQL should detect this vulnerability with:
- **Alert Type**: SQL Injection (CWE-89)
- **Severity**: High or Critical
- **Query**: `py/sql-injection` or similar
- **Description**: Database query built from user-controlled sources

### CodeQL Query Suite
The repository uses `security-extended` queries in `.github/workflows/codeql.yml`:
```yaml
queries: security-extended
```

This comprehensive query suite should definitely catch SQL injection vulnerabilities.

### Why CodeQL Will Detect This
1. **Taint Tracking**: CodeQL tracks data flow from untrusted sources (`request.args.get()`) to SQL sinks (`conn.execute()`)
2. **Pattern Recognition**: Detects string concatenation used to build SQL queries
3. **Dataflow Analysis**: Identifies that user input flows directly into SQL execution without sanitization

## Remediation (DO NOT APPLY - For Reference Only)

To fix this vulnerability, the code should use parameterized queries:

```python
@app.route('/search')
def search_user():
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    
    if search_query:
        # SAFE: Using parameterized query with ? placeholders
        query = "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?"
        search_param = f"%{search_query}%"
        users = conn.execute(query, (search_param, search_param)).fetchall()
    else:
        users = conn.execute('SELECT * FROM users').fetchall()
    
    conn.close()
    return render_template('index.html', users=users, search_query=search_query)
```

## Security Impact Assessment

### CVSS Considerations
- **Attack Vector**: Network (exploitable via HTTP request)
- **Attack Complexity**: Low (simple payload)
- **Privileges Required**: None (public endpoint)
- **User Interaction**: None
- **Confidentiality Impact**: High (can read all data)
- **Integrity Impact**: High (can modify data)
- **Availability Impact**: Low (can cause DoS in some scenarios)

### Real-World Impact
In a production environment, this vulnerability could lead to:
- Unauthorized data access
- Data breach and exfiltration
- Data manipulation or deletion
- Authentication bypass
- Potential for complete database compromise

## Conclusion

This intentional SQL injection vulnerability provides a clear test case for CodeQL's static analysis capabilities. The vulnerability is:
- **Obvious**: Direct string concatenation with user input
- **Exploitable**: Multiple attack vectors demonstrated
- **Detectable**: Should be caught by CodeQL's security-extended queries
- **Well-documented**: Clear examples and explanations provided

The CodeQL SAST workflow should flag this issue when the code is pushed or when a pull request is created against the main/master branch.
