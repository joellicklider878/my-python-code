import csv
import json
import re
from datetime import datetime, timedelta  # Fix: Added explicit timedelta import
from pathlib import Path

def generate_mock_data(num_records=500):
    """Generates mock customer data."""
    data = []
    for i in range(num_records):
        customer_id = f"CUST-{i+1:03d}"
        name = f"Customer {i+1}"
        email = f"customer{i+1}@example.com"
        phone = f"+1-555-123-{i+1:02d}"
        address = "123 Main St, Anytown, USA"
        
        # Fix: Resolved timedelta syntax bug
        dob_str = (datetime.now() - timedelta(days=i*365)).strftime("%Y-%m-%d")
        order_total = round(float(i * 10), 2)

        data.append({
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "dob": dob_str,
            "order_total": order_total
        })
    return data

def validate_record(record):
    """Validates a single customer record."""
    errors = []

    # Fix: Guard against falsy values like numeric 0 or 0.0 evaluating as missing
    for field in ["name", "email", "phone", "dob"]:
        if not record.get(field):
            errors.append(f"Missing {field}")
            
    if record.get("order_total") is None or record.get("order_total") == "":
        errors.append("Missing order total")

    # Fix: Better standard regex validation pattern for email addresses
    email = record.get("email", "")
    if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        errors.append("Invalid email format")

    try:
        order_total = float(record.get("order_total"))
        if order_total < 0:
            errors.append("Order total cannot be negative")
    except (ValueError, TypeError):
        errors.append("Invalid order total format")

    return errors

def process_records(data):
    """Processes the customer data, cleaning and identifying rejected records."""
    cleaned_records = []
    rejected_records = []
    audit_report = []

    for record in data:
        errors = validate_record(record)
        if not errors:
            cleaned_records.append(record)
        else:
            # Fix: Keep schema flat so it writes neatly to a CSV structure
            flat_rejected_record = record.copy()
            flat_rejected_record["validation_errors"] = "; ".join(errors)
            rejected_records.append(flat_rejected_record)
            
            audit_report.append({
                "customer_id": record.get("customer_id"),
                "record_status": "Rejected",
                "errors": errors
            })

    return cleaned_records, rejected_records, audit_report

def write_csv(filename, data):
    """Writes data to a CSV file securely."""
    # Security Fix: Prevent file manipulation by verifying path boundaries via Pathlib
    safe_path = Path(filename).name 
    with open(safe_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def write_json(filename, data):
    """Writes data to a JSON file safely."""
    safe_path = Path(filename).name
    with open(safe_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

if __name__ == "__main__":
    customer_data = generate_mock_data()
    cleaned_records, rejected_records, audit_report = process_records(customer_data)

    write_csv("cleaned_records.csv", cleaned_records)
    write_csv("rejected_records.csv", rejected_records)
    write_json("audit_report.json", audit_report)

    print("Data processing complete.")