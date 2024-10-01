import re
import html
import bs4
from so_api import get_api_answer
import ChatGBT_db.devgpt_chats as chatgpt_db


def remove_non_utf8_chars(text):
    # Step 1: Unescape any HTML entities
    unescaped_text = html.unescape(text)

    # Step 2: Decode Unicode escape sequences to actual characters
    try:
        decoded_text = unescaped_text.encode().decode('unicode_escape')
    except (UnicodeDecodeError, AttributeError):
        decoded_text = unescaped_text  # Fall back to original if decoding fails

    # Step 3: Use regex to remove non-ASCII and non-basic Unicode characters
    clean_text = re.sub(r'[^\x00-\x7F]+', '', decoded_text)

    return clean_text


def extract_html_code(body):
    # Parse the HTML content
    soup = bs4.BeautifulSoup(chatgpt_db.json_data_to_str(body), 'html.parser')

    # Extract the code snippets within <pre><code> tags
    code_snippets = [pre.get_text() for pre in soup.find_all('pre')]

    # Concatenate all extracted code snippets
    code = "\n".join(code_snippets)

    return code


# Test the API answer
so_api_answer_body = get_api_answer([79018992])
extracted_code = extract_html_code(so_api_answer_body)

print("Cleaned Code Output:")
#print(extracted_code)
cleaned_code = remove_non_utf8_chars(extracted_code)
print(cleaned_code)
