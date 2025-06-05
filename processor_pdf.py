import pdfplumber
import json


def extract_table(filename):
    rows = []
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            rows.append(text.split("\n"))
    return rows[0][1:]


def format_rows(rows):
    split_rows = []
    for row in rows:
        parts = row.split(' ')
        index = parts[0]
        income = parts[-1]
        fio = " ".join(parts[1:-1])
        split_rows.append([index, fio, income])
    return split_rows


def write_json(rows):
    output = []
    for row in rows:
        data = {'client_id': row[0], 'client_FIO': row[1], 'credit_income': row[2]}
        output.append(data)

    return json.dumps(output, ensure_ascii=False, indent=4)


def process_file(filename):
    rows = format_rows(extract_table(filename))
    json_string = write_json(rows)
    return json_string

