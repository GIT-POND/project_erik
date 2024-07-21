import categorize_csv.categorize as categorize
import pdf_to_csv.pdf_to_xlsx_taxes_v2 as read_pdf
import misc.main as helpers


# helpers.main() # do not uncomment


read_pdf.main()
categorize.main()