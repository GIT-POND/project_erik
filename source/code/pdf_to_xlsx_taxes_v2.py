import os
import PyPDF2
import pandas as pd

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

if __name__ == "__main__":
    input_folder = "C:/Users/tanoo/OneDrive/Desktop/project_erik/insert_woodforest_pdfs_here/" # Folder containing PDF files
    output_excel_path = "C:/Users/tanoo/OneDrive/Desktop/project_erik/raw_output.csv"  # Desired output Excel file path

    if not os.path.exists(input_folder):
        print(f"Folder {input_folder} does not exist.")
    else:
        all_lines = list()

        # Loop through all PDF files in the input folder
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".pdf"):
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
        
        df.to_csv(output_excel_path, index=False)
        print(f"Combined data has been saved to {output_excel_path}")