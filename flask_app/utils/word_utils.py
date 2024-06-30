from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from enums import ReportEnums
import uuid 

def replace_bookmarks(doc_path, replacements, tables_rows=None):
    try:
        doc = Document(doc_path)

        for paragraph in doc.paragraphs:
            for bookmark_name in replacements:
                if f'<{bookmark_name}>' in paragraph.text:
                    paragraph.text = paragraph.text.replace(f'<{bookmark_name}>', str(replacements[bookmark_name]))
        
        if tables_rows:
            fill_tables(doc, tables_rows)

        new_file_path = ReportEnums.TEMPLATE_PATH.value + f'/{str(uuid.uuid1())} + .docx'
        doc.save(new_file_path)
        return True, new_file_path
    
    except Exception as e:
        # raise e
        return False, doc_path
    
def fill_tables(doc, table_data):
    if not table_data:
        return False

    # Find the paragraph containing the <TABLE> placeholder
    for paragraph in doc.paragraphs:
        if '<TABLE>' in paragraph.text:
            # Remove the old paragraph containing the bookmark
            p = paragraph._element
            p.getparent().remove(p)

            # Create a new table
            headers = list(table_data[0].keys())
            table = doc.add_table(rows=1, cols=len(headers))  # Create table with header row
            table.autofit = False  # Disable autofit for manual control

            # Set custom column widths
            col_widths = [Inches(1.5)] * len(headers)  # Adjust width as needed
            for i, col in enumerate(table.columns):
                col.width = col_widths[i]

            # Add table headers dynamically from the first row keys
            hdr_cells = table.rows[0].cells
            for i, header_text in enumerate(headers):
                hdr_cells[i].text = header_text
                hdr_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                run = hdr_cells[i].paragraphs[0].runs[0]
                font = run.font
                font.size = Pt(12)  # Larger font size for better visibility
                font.bold = True

            # Add table rows
            for row_data in table_data:
                row_cells = table.add_row().cells
                for i, (header, cell_value) in enumerate(row_data.items()):
                    row_cells[i].text = str(cell_value)
                    row_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    run = row_cells[i].paragraphs[0].runs[0]
                    font = run.font
                    font.size = Pt(12)  # Larger font size for better visibility

            return True

    # If no bookmark <TABLE> is found
    return False