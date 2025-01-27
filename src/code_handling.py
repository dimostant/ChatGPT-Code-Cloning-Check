import os
import re
import bs4
import html
import subprocess
import tempfile
from src.ChatGBT_db.devgpt_chats import json_data_to_str


def extract_html_text(body):
    body_to_str = json_data_to_str(body)
    soup = bs4.BeautifulSoup(body_to_str, 'html.parser')
    text = soup.get_text()

    return text

def extract_html_code(body):
    # Parse the HTML content
    body_to_str = json_data_to_str(body)
    soup = bs4.BeautifulSoup(body_to_str, 'html.parser')

    # Find all code snippets inside <pre><code> tags
    code_snippets = [pre.get_text() for pre in soup.find_all('pre')]

    # TODO: need to check the order of the concat
    #  Find all inline code snippets inside <code> tags not within <pre>
    #  needs testing, e.g <pre><code>1<code>2</code>3</pre></code>, is it in order?
    #  probably not needed, needs testing
    # inline_code_snippets = [code.get_text() for code in soup.find_all('code') if code.parent.name != 'pre']

    # Combine all extracted code snippets
    code = "\n".join(code_snippets)#  + inline_code_snippets) #this relates to the line 78 issue

    return code

def extract_dictionary_code(dictionary):
    code = "\n".join([block["Content"] for block in dictionary])
    return code

def remove_ansi_escape_sequences(text):
    ansi_escape_text = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape_text.sub('', text)

def remove_non_utf8_chars(text):
    # Unescape any HTML entities
    unescaped_text = html.unescape(text)

    # Decode Unicode escape sequences to actual characters
    try:
        decoded_text = unescaped_text.encode().decode('unicode_escape')
    except (UnicodeDecodeError, AttributeError):
        decoded_text = unescaped_text  # Fall back to original if decoding fails

    # Use regex to remove non-ASCII and non-basic Unicode characters
    return re.sub(r'[^\x00-\x7F]+', '', decoded_text)

def calculate_clone_percentage(simian_output):
    duplicate_lines_line = re.search(r'Found \d+ duplicate lines in \d+ blocks in \d+ files', simian_output)
    if not duplicate_lines_line:
        duplicate_lines = 0
    else:
        duplicate_lines = int(re.search(r'\d+', duplicate_lines_line.group()).group())

    print(duplicate_lines)
    total_lines_line = re.search(r'Processed a total of \d+ significant \((\d+) raw\) lines in \d+ files',
                                 simian_output)
    if not total_lines_line:
        total_lines = 0
    else:
        total_lines = int(re.search(r'\d+', total_lines_line.group()).group())

    print(total_lines)

    if total_lines != 0:
        return (duplicate_lines / total_lines) * 100

def code_cloning_check(gpt_answer_code, so_api_answer_code):
    print("\ncomparing answers :\n", gpt_answer_code.replace("\n", " "), "\nand :\n", so_api_answer_code.replace("\n", " "))

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code1_file, \
         tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code2_file:

        code1_file.write(gpt_answer_code.encode('ascii'))
        code2_file.write(so_api_answer_code.encode('ascii'))

        code1_file.seek(0)
        code2_file.seek(0)

        code1_file.close()
        code2_file.close()

    try:
        simian = subprocess.run(
            ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", code1_file.name, code2_file.name],
            text=True, capture_output=True # check=True
        )

        simian_output = ''.join(simian.stdout.splitlines(keepends=True)[4:-1])

    finally:
        os.remove(code1_file.name)
        os.remove(code2_file.name)

    return calculate_clone_percentage(simian_output)