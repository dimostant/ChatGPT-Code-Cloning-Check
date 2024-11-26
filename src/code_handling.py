import ast
import re

import bs4
import ChatGBT_db.devgpt_chats as chatgpt_db

import html

def is_valid_python_code(code):
    try:
        # Try parsing the code using ast.parse
        ast.parse(code)
        return True
    except SyntaxError:
        # If there is a syntax error, it means the code is not valid Python
        return False

def extract_html_text(body):
    body_to_str = chatgpt_db.json_data_to_str(body)
    soup = bs4.BeautifulSoup(body_to_str, 'html.parser')
    text = soup.get_text()

    return text

def extract_html_code(body):
    # Parse the HTML content
    body_to_str = chatgpt_db.json_data_to_str(body)
    soup = bs4.BeautifulSoup(body_to_str, 'html.parser')

    # Find all code snippets inside <pre><code> tags
    code_snippets = [pre.get_text() for pre in soup.find_all('pre')]

    # TODO: need to check the order of the concat
    # Find all inline code snippets inside <code> tags not within <pre>
    # inline_code_snippets = [code.get_text() for code in soup.find_all('code') if code.parent.name != 'pre']
    # TODO: needs testing, e.g <pre><code>1<code>2</code>3</pre></code>, is it in order?
    # probably not needed needs testing

    # Combine all extracted code snippets
    code = "\n".join(code_snippets)#  + inline_code_snippets) #this relates to the line 78 issue

    return code

def extract_dictionary_code(dictionary):
    code = "\n".join([block["Content"] for block in dictionary])
    return code


def remove_non_utf8_chars(text):
    # Unescape any HTML entities
    unescaped_text = html.unescape(text)

    # Decode Unicode escape sequences to actual characters
    try:
        decoded_text = unescaped_text.encode().decode('unicode_escape')
    except (UnicodeDecodeError, AttributeError):
        decoded_text = unescaped_text  # Fall back to original if decoding fails

    # Use regex to remove non-ASCII and non-basic Unicode characters
    clean_text = re.sub(r'[^\x00-\x7F]+', '', decoded_text)

    return clean_text
