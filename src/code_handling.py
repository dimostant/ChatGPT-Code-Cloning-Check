import re
import bs4
import html
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


def clean_text(text):
    # Unescape any HTML entities
    unescaped_text = html.unescape(text)

    # Decode Unicode escape sequences to actual characters
    try:
        decoded_text = unescaped_text.encode().decode('unicode_escape')
    except (UnicodeDecodeError, AttributeError):
        decoded_text = unescaped_text  # Fall back to original if decoding fails

    # Use regex to remove non-ASCII and non-basic Unicode characters
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', decoded_text)

    ansi_escape_text = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    ansi_escape_text.sub('', cleaned_text)

    return  ansi_escape_text.sub('', cleaned_text)