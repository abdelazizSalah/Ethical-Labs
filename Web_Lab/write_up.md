# Lab4: SQL Injections and XSS attacks

## 📄 Brief Summary of the Document:

This document is Task Sheet 04 for the Cyber Security Lab (Ethical Hacking) course at BTU, Summer Term 2025. It focuses on web security, specifically SQL Injection (SQLi) and Cross-Site Scripting (XSS) vulnerabilities in a demo web application.

We are given a simple forum-like PHP web app (hosted via Docker) and must:

- Exploit it like a black-box attacker (i.e., without looking at source code until the final task).

-  Perform several practical attacks (SQLi, XSS, session hijacking).

-   Demonstrate full exploitation and eventually fix the vulnerabilities.

## ✅ What We Need to Do – Task Overview
✔️ Task 1: SQL Injection – Get Admin Password

- Use SQLi to dump the admin user’s password.

-   Log in as admin and post a comment.

-   Export all users and passwords to users.txt.

✔️ Task 2: SQL Injection – List Hidden Pages

-   Find and list hidden URLs/pages in the app via SQLi (e.g., stats.php).

-   Document whether they need authentication.

-   Save page list to pages.txt.

✔️ Task 3: Discover Reflected XSS

-   Test the statistical page’s search field for reflected XSS.

-   Identify encoding, HTTP method, and data structure used.

✔️ Task 4: Session Hijacking via Reflected XSS

-   Create a malicious URL using the reflected XSS to steal session cookies.

-   Use a simple HTTP server (e.g., python3 -m http.server) to receive the data.

-   Prove the session theft by accessing the app as the victim (e.g., ada).

✔️ Task 5: Persistent XSS and Self-Propagation

-   Exploit XSS to post a malicious comment that auto-runs for future visitors.

-   Handle CSRF token and comment-posting logic in exploit.js.

-   Goal: Once a victim clicks the malicious link, all users are infected.

✔️ Task 6: Fix the Code

-   Now We can analyze the server-side PHP code.

-   Identify and fix the root causes of all previous vulnerabilities.

## What is SQLi?
SQL Injection (SQLi) is a type of code injection attack where an attacker inserts malicious SQL commands into input fields of a web application. These commands are then unknowingly executed by the backend database server.

This happens when user input is not properly sanitized or validated, allowing the attacker to manipulate the structure of SQL queries. As a result, the attacker may be able to:

-   🕵️‍♂️ View sensitive data (e.g., usernames, passwords, credit card numbers)

-   ✏️ Modify or delete database entries

-   🚪 Bypass authentication systems

-   💣 Drop entire tables or databases


## What is XSS?
Cross-Site Scripting (XSS) is a type of security vulnerability found in web applications that allows an attacker to inject malicious scripts (usually JavaScript) into webpages viewed by other users.

This can happen when the application takes user input (e.g., comments, search fields) and displays it on the page without proper filtering or encoding.

### ⚠️ Why is XSS Dangerous?

Once the malicious script runs in the victim’s browser, it can:

- 🥷 Steal cookies or session tokens (used for login)

-   📋 Read private data

-   🔗 Redirect the victim to malicious sites

-   🧠 Pretend to be the user and perform actions on their behalf

### 🎯 Types of XSS

-   Reflected XSS:
    - The script is part of the URL or request, and it’s reflected back in the server response.

    -  Triggered when a victim clicks a specially crafted link.

- Stored (Persistent) XSS:
    - The script is saved in the database (e.g., in a comment), and it runs every time someone views that page.

    -  Very powerful; affects multiple users.

- DOM-based XSS:
    -   The vulnerability is in the client-side JavaScript, not the server.

    -  Happens when the browser’s DOM is manipulated without sanitizing input.


## Tasks Solutions: 
### Task1: Obtaining the Admin Password
- In order to do so, we first must check whether there is a SQL injection vulnerability or not, so this can be done by excuting some try and error sql commands and see if we can see any errors:
    - ![alt text](image.png)
- in the above screenshot we can see that on inserting wrong inputs in the login field, it says that SQLite error, this means that we are dealing with **SQLite** database and there is a vulnerability.
- so my first suspection will be that it uses such command:
    - "SELECT * FROM users WHERE username = '$username_from_input' and password = '$password_from_input'";
- so my first trial will be to use this command: 
    > ' OR 1=1 -- 
- to try to bypass the password check, but unfortunatly it did not work

- so lets try to know what is the used database scheme:
    > ' UNION SELECT name FROM sqlite_master WHERE type='table' --
- on excuting this I got the following results: 
    - ![alt text](image-2.png)
- it shows that we have 2 tables which are:    
    - pages
    - users
- now we are more interested in the **users** table, so we need to know its columns names
    > ' UNION SELECT sql FROM sqlite_master WHERE name='users' --
- on excuting this query we can see that he users table consists of 2 columns which are: 
    - name
    - password
    - ![alt text](image-3.png)
- now we need to select all entries
    > ' UNION SELECT name || ':' || password FROM users --
- on excuting the above command we can see that we can extract the whole entries in the table: 
    - ![alt text](image-4.png)

### Task2: Listing the Pages of the Web Application