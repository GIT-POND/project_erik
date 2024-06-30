import os
import PyPDF2
import pandas as pd
from collections import defaultdict

all_lines = list()

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

    return text.split("\n")


if __name__ == "__main__":
    input_folder = "C:/Users/tanoo/OneDrive/Desktop/WNBStatement.pdf"  # Folder containing PDF files
    output_excel_path = "C:/Users/tanoo/OneDrive/Desktop/output.xlsx"  # Desired output Excel file path

    if not os.path.exists(input_folder):
        print(f"Folder {input_folder} does not exist.")
    else:
        lines = read_pdf(input_folder)
        indices = [i for i, x in enumerate(lines) if (x == "Transactions " or "TW100T01282307030700-30" in x or "Transactions (continued)" in x)]
        data_lines = list()

        for x in range(0, len(indices)-1, 2):
            data_lines += lines[indices[x]+1: indices[x+1]]
        
        format_data_lines = [line.split(maxsplit=3) for line in data_lines[0:155]]
        final_lines = list();
        
        for line in format_data_lines:
            if ("Balance Description" not in line[3]):
                if ("ACH-SQUIRE Pay" in line[3] or "POS CR" in line[3] or "ACH-CASHOUT" in line[3] or "ACH-* Cash App" in line[3]):
                    final_lines.append([line[0], line[1], '', line[2], line[3]])
                else: 
                    final_lines.append([line[0], '', line[1], line[2], line[3]])
            
        # print(final_lines)
        
        columns = ['Date', 'Credits', 'Debits', 'Balance', 'Description']
        
        df = pd.DataFrame(final_lines, columns = columns)
        
        df.to_csv(output_excel_path, index=True)