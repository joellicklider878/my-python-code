# User Authentication & Secure Password Management Utility

A Python implementation demonstrating secure password lifecycle management—including cryptographic hashing, secure verification, token parsing, and automated unit testing. 

This repository showcases secure coding best practices by using industry-standard key derivation functions (PBKDF2) paired with protection against timing attacks.

## Features

- **Secure Cryptographic Hashing:** Uses `PBKDF2-HMAC-SHA256` with a high-iteration count (600,000 iterations) and uniquely generated 16-byte random salts (`os.urandom`) to mitigate rainbow table attacks.
- **Timing-Attack Resistance:** Employs `hmac.compare_digest` for password verification to ensure constant-time string comparisons.
- **Account Security Mechanics:** Built-in hooks for validation logic, including brute-force prevention (tracking failed logins) and account ban checks.
- **Password Reset Pipeline:** Outlines the core functions needed to safely parse, look up, and process token-based password resets via an external email flow.
- **Unit Testing Framework:** Built-in test suite using `unittest` and `unittest.mock` to validate cryptographic flows and database state modifications without needing a live database connection.

## Architecture & Security Standards

- **Salt Size:** 16 bytes of cryptographically secure random data per user.
- **Iterations:** 600,000 rounds (aligned with modern OWASP recommendations).
- **Comparison Engine:** Constant-time bitwise matching via `hmac`.

## Getting Started

### Prerequisites

This utility utilizes Python standard libraries (`hashlib`, `hmac`, `secrets`, `unittest`) and has no external package dependencies.

### Running the Test Suite

The script comes embedded with localized test runners to verify that password mutations and database commits function exactly as intended. Execute the module directly from your terminal:

```bash
python script.py
```

## Code Map & Key Functions

### 1. Cryptographic Handlers
* **`update_user_password(user, new_password)`**: Generates a new salt, hashes the incoming string, updates the user object attributes, and commits to the database session.
* **`verify_user_password(user, input_password)`**: Re-hashes incoming login credentials using the user's specific salt to verify validity using constant-time evaluation.

### 2. Session & Lifecycle Hooks
* **`check_user_legitimacy(user)`**: Evaluates security criteria (e.g., flags account as false if `failed_logins > 5` or `banned == True`).
* **`validate_user_credentials(email, password)`**: Handles database filters to resolve matching profiles.
* **`parse_reset_token(request)`** / **`lookup_reset_token(token)`**: Handles incoming API requests to check token integrity against a 1-hour expiration matrix.

## Contribution & Disclaimer

*Note: This architecture utilizes a mock database wrapper (`MockDB`) for standard simulation. Integrate this utility with an active Object-Relational Mapper (such as SQLAlchemy) within your production backend environment.*
