# table_extractor.py
import pdfplumber
# def detect_tables(pdf_path):
#     """
#     Detect tables in a PDF file.
    
#     - Uses pdfplumber's built-in method for tables with borders.
#     - Uses custom logic for borderless/irregular tables.

#     Args:
#         pdf_path (str): Path to the PDF file.
    
#     Returns:
#         list: A list of detected tables, each containing table metadata.
#     """
#     detected_tables = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_number = page.page_number
#             page_tables = []

#             # Detect tables using pdfplumber's built-in method
#             built_in_tables = page.find_tables()
#             if built_in_tables:
#                 for table in built_in_tables:
#                     page_tables.append({
#                         "page_number": page_number,
#                         "method": "built_in",
#                         "bbox": table.bbox,
#                         "table_object": table
#                     })
#             else:
#                 # Try detecting tables using text alignment heuristics
#                 words = page.extract_words()
#                 grouped_lines = group_words_by_line(words)
#                 candidate_lines = [line for line in grouped_lines if len(line) >= 3]

#                 if candidate_lines:
#                     page_tables.append({
#                         "page_number": page_number,
#                         "method": "heuristic",
#                         "lines": candidate_lines
#                     })

#             if page_tables:
#                 detected_tables.extend(page_tables)

#     return detected_tables

def extract_tables(pdf_path, detected_tables):
    """
    Extract table data from detected table regions.

    Args:
        pdf_path (str): Path to the PDF file.
        detected_tables (list): A list of detected tables (from table_detector.py).
    
    Returns:
        list: A list of tables, where each table is a list of rows (each row is a list of strings).
    """
    extracted_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for table_info in detected_tables:
            page_number = table_info["page_number"]
            page = pdf.pages[page_number - 1]  # pdfplumber uses 0-based indexing

            if table_info["method"] == "built_in":
                # Extract bordered table data
                table_obj = table_info["table_object"]
                table_data = table_obj.extract()  # Extracts as a list of rows
                if table_data:
                    extracted_tables.append(table_data)
            elif table_info["method"] == "heuristic":
                # Extract borderless table using custom logic
                candidate_lines = table_info["lines"]
                table_data = extract_table_from_lines(candidate_lines)
                if table_data:
                    extracted_tables.append(table_data)

    return extracted_tables

def extract_table_from_lines(lines):
    """
    Processes candidate lines (list of words) to form structured table rows.

    Args:
        lines (list): List of word dictionaries representing detected lines.

    Returns:
        list: A list of rows (each row is a list of cell values).
    """
    table_rows = []
    for line in lines:
        # Sort words in the line by their 'x0' position (left-to-right order)
        sorted_words = sorted(line, key=lambda w: w['x0'])
        row = merge_words_into_columns(sorted_words)
        table_rows.append(row)
    return table_rows

def merge_words_into_columns(words, gap_threshold=10):
    """
    Merges words into columns based on horizontal spacing.
    
    If the gap between words is larger than `gap_threshold`, it is considered a column break.

    Args:
        words (list): A sorted list of words in a row.
        gap_threshold (float): Minimum horizontal gap to detect column breaks.

    Returns:
        list: A list of text values representing table columns.
    """
    if not words:
        return []

    columns = []
    current_column = words[0]['text']
    prev_x1 = words[0]['x1']

    for word in words[1:]:
        gap = word['x0'] - prev_x1
        if gap > gap_threshold:
            # Column break detected, start a new column
            columns.append(current_column.strip())
            current_column = word['text']
        else:
            # Continue adding to the same column
            current_column += " " + word['text']
        prev_x1 = word['x1']

    columns.append(current_column.strip())  # Append the last column
    return columns

# For testing
if __name__ == "__main__":
    from detect import detect_tables

    pdf_path = "test6.pdf"  # Change to your test file
    detected_tables = detect_tables(pdf_path)
    tables = extract_tables(pdf_path, detected_tables)

    for idx, table in enumerate(tables):
        print(f"\n--- Table {idx+1} ---")
        for row in table:
            print(row)
