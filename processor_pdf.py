import pdfplumber
import json


def extract_table(filename):
    rows = []
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            for row in table:
                rows.append(row)
    return rows[1:]


def format_rows(rows):
    for row in rows:
        if ' ' in row[2]:
            parts = row[2].split(' ')
            row[1] += parts[0]
            row[2] = parts[1]
    return rows


def write_json(rows):
    output = []
    for row in rows:
        data = {'client_id': row[0], 'client_FIO': row[1], 'credit_income': format(float(row[2]), ".2f")}
        output.append(data)

    return json.dumps(output, ensure_ascii=False, indent=4)


def process_file(filename):
    rows = format_rows(extract_table(filename))
    json_string = write_json(rows)
    return json_string

