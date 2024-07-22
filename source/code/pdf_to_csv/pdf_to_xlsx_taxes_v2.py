import os
import PyPDF2
import pandas as pd

def getInputDir():
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    input_dir = os.path.join(source_dir, "input_files")

    return input_dir

def getOutputPath(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "output_files")

    return os.path.join(file_dir, file_name)

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text.split("\n")

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def main():
    input_folder = getInputDir()
    output_excel_path = getOutputPath("raw_output.csv")  # Desired output Excel file path

    if not os.path.exists(input_folder):
        print(f"Folder {input_folder} does not exist.")
    else:
        all_lines = list()

        # Loop through all PDF files in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".pdf"):
                print('file name:',file_name)
                file_path = os.path.join(input_folder, file_name)
                lines = read_pdf(file_path)
                indices = [i for i, x in enumerate(lines) if (x == "Transactions " or "TW100T01282307030700-30" in x or "Transactions (continued)" in x)]
                data_lines = list()

                for x in range(0, len(indices)-1, 2):
                    data_lines += lines[indices[x]+1: indices[x+1]]
                
                all_lines.extend(data_lines)

        format_data_lines = [line.split(maxsplit=3) for line in all_lines if line.strip()]
        final_lines = list()
        
        for line in format_data_lines:
            if len(line) < 4:
                continue
            if "Balance Description" not in line[3] and has_numbers(line[0]) :
                if "ACH-SQUIRE Pay" in line[3] or "POS CR" in line[3] or "ACH-CASHOUT" in line[3] or "ACH-* Cash App" in line[3]:
                    final_lines.append([line[0], line[1], '', line[2], line[3]])
                else: 
                    final_lines.append([line[0], '', line[1], line[2], line[3]])
        
        columns = ['Date', 'Credits', 'Debits', 'Balance', 'Description']
        df = pd.DataFrame(final_lines, columns=columns)
        
        print('lines:',final_lines)
        df.to_csv(output_excel_path, index=False)
        # print(f"\n\nCompiled PDF data written to: {output_excel_path}\n\n")