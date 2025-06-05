from img2table.document import Image
from img2table.ocr import TesseractOCR
import json


def extract_table(filename):
    image = Image(filename, detect_rotation=False)
    ocr = TesseractOCR(n_threads=1, lang='eng+rus')

    table = image.extract_tables(ocr=ocr)
    return table[0].df


def write_json(df):
    output = []
    for _, row in df.iloc[1:].iterrows():
        data = {'client_id': row[0], 'client_FIO': row[1], 'credit_income': row[2]}
        output.append(data)

    return json.dumps(output, ensure_ascii=False, indent=4)


def process_file_jpg(filename):
    df = extract_table(filename)
    json_string = write_json(df)
    return json_string
