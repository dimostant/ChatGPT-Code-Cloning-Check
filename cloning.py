#import pandas as pd
#import requests
#from bs4 import BeautifulSoup
#from difflib import SequenceMatcher
#from requests.exceptions import ConnectTimeout, HTTPError

#to use the code from the refference
#to be well tested

def code_cloning_check(gpt_answer_code, so_api_answer_code):
    print("\ncomparing answers :\n", gpt_answer_code.replace("\n", " "), "\nand :\n", so_api_answer_code.replace("\n", " "))
    # insert code to abstract syntax tree (python code only!)??
    # tree1 = ast.parse(extracted_so_api_code)
    # tree2 = ast.parse(gpt_answer_clean_code)
    print("cloning or not cloning idk lmao!!!!...")

# def get_webpage_text(url):
#     url = url.lstrip('\ufeff')
#     try:
#         response = requests.get(url, timeout=5)  # Set a timeout value in seconds
#         response.raise_for_status()  # Raise an error for bad responses
#         soup = BeautifulSoup(response.text, 'html.parser')
#         return soup.get_text()
#     except ConnectTimeout as e:
#         print(f"Error connecting to {url}: {e}")
#         return ""
#     except HTTPError as e:
#         print(f"HTTP Error {e.response.status_code} for {url}: {e}")
#         return ""
#
# def preprocess_text(text):
#     lines = text.splitlines()
#     non_empty_lines = [line for line in lines if line.strip()]
#     return ' '.join(non_empty_lines)
#
# def code_similarity(code_block, webpage_text):
#     similarity_ratio = SequenceMatcher(None, code_block, webpage_text).ratio()
#     return similarity_ratio
#
# def find_similar_lines_with_context(code, webpage_text):
#     similar_lines_with_context = []
#
#     for line in code.splitlines():
#         parts = line.split('\x0b')
#         for part in parts:
#             part_strip = part.strip()
#             if part_strip in webpage_text and part_strip not in similar_lines_with_context:
#                 similar_lines_with_context.append((part_strip, webpage_text))
#
#     return similar_lines_with_context
#
#
# def count_lines_in_webpage(code, webpage_text):
#     code_lines = code.splitlines() if isinstance(code, str) else []
#     count = 0
#     counter = 0
#
#     for line in code_lines:
#         parts = line.split('\x0b')
#         for part in parts:
#             counter += 1
#             print("", counter, ":", part.strip(), "\n")
#             if part.strip() in webpage_text:
#                 count += 1
#
#     return count, counter
#
# # Input Excel file path
# excel_file_path = "/Users/anastassia/Desktop/SYNEDRIA/icsr24/DevGPT2/snapshot_20230831/rr_output.xlsx"
# # Print message indicating the file is being opened
# print(f"Opening Excel file: {excel_file_path}")
#
# # Read the Excel file into a DataFrame
# df = pd.read_excel(excel_file_path)
#
# # Create new columns for the additional information
# df['Lines_Count'] = 0
# df['Counter'] = 0
# df['Usage_Ratio'] = 0.0
# df['Similar_Lines_Web'] = ""
# df['Similarity_Web'] = 0.0
#
# ## Iterate through rows and perform modifications
# for index, row in df.iterrows():
#     if "commit" in row['Type'].lower() or "pull request" in row['Type'].lower():
#         web_url = row['URL'] + "/files"
#         code = row['Different_Lines_Column2']
#
#         print("Columns url:")
#         print(web_url)
#         print("Columns code:")
#         print(code)
#
#         # Check for NaN values in 'Code_Column2'
#         if pd.notna(code):
#             webpage_text = get_webpage_text(web_url)
#             if not webpage_text:  # If webpage_text is empty or an error occurred
#                 print(f"Skipping further processing for {web_url}")
#                 continue
#
#             code_lines = code.splitlines()
#             code_text = preprocess_text('\n'.join(code_lines))
#             webpage_text = preprocess_text(webpage_text)
#             # Calculate similarity ratio
#             similarity_ratio = code_similarity(code_text, webpage_text)
#
#             # Find similar lines with context and calculate similarities
#             similar_lines_with_context = find_similar_lines_with_context(code_text, webpage_text)
#
#             # Calculate the usage ratio
#             usage_ratio = len(similar_lines_with_context) / len(code_lines) if len(code_lines) != 0 else 0
#
#             # Update the values in the DataFrame
#             df.at[index, 'Usage_Ratio'] = usage_ratio
#
#             # Store similar lines with context
#             similar_lines_str = ", ".join([f"{line} (Web: {webpage_line})" for line, webpage_line in similar_lines_with_context])
#             df.at[index, 'Similar_Lines_Web'] = similar_lines_str
#
#             # Store similarity ratio with context
#             df.at[index, 'Similarity_Web'] = similarity_ratio
#
#
#             lines_count, counter = count_lines_in_webpage(code, webpage_text)
#             df.at[index, 'Lines_Count'] = lines_count
#             df.at[index, 'Counter'] = counter
#
#
#
#
# # Save the modified DataFrame back to the Excel file
# output_excel_file_path = '/Users/anastassia/Desktop/SYNEDRIA/icsr24/DevGPT2/snapshot_20230831/rrweb_output.xlsx'
# df.to_excel(output_excel_file_path, index=False)
#
# print(f"Results written to {output_excel_file_path}")
