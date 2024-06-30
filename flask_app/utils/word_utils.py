from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import uuid 

def replace_bookmarks(doc_path, replacements, tables_rows=None):
    try:
        doc = Document(doc_path)

        for paragraph in doc.paragraphs:
            for bookmark_name in replacements:
                if f'<{bookmark_name}>' in paragraph.text:
                    paragraph.text = paragraph.text.replace(f'<{bookmark_name}>', replacements[bookmark_name])
        
        if tables_rows:
            fill_tables(doc, tables_rows)

        new_file_path = str(uuid.uuid1()) + '.docx'
        doc.save(new_file_path)
        return True, new_file_path
    except Exception as e:
        raise e
        return False, doc_path

def fill_tables(doc, tables):
    for bookmark_name, table_data in tables.items():
        if bookmark_name == '<TABLE>':
            # Find the paragraph containing the bookmark placeholder
            for paragraph in doc.paragraphs:
                if '<TABLE>' in paragraph.text:
                    # Remove the old paragraph containing the bookmark
                    p = paragraph._element
                    p.getparent().remove(p)
                    
                    # Create a new table
                    table = doc.add_table(rows=1, cols=len(table_data[0]))  # Assuming table_data[0] contains headers
                    table.autofit = True
                    
                    # Add table headers
                    hdr_cells = table.rows[0].cells
                    for i, header_text in enumerate(table_data[0]):
                        hdr_cells[i].text = header_text
                        hdr_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                        run = hdr_cells[i].paragraphs[0].runs[0]
                        font = run.font
                        font.size = Pt(10)
                        font.bold = True
                        
                    # Add table rows
                    for row_data in table_data[1:]:
                        row_cells = table.add_row().cells
                        for i, cell_value in enumerate(row_data):
                            row_cells[i].text = cell_value
                            row_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                            run = row_cells[i].paragraphs[0].runs[0]
                            font = run.font
                            font.size = Pt(10)

                    # Save the modified document
                    return True

    # If no bookmark <TABLE> is found
    return False