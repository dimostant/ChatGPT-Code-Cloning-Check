import ast

def is_valid_python_code(code):
    try:
        # Try parsing the code using ast.parse
        ast.parse(code)
        return True
    except SyntaxError:
        # If there is a syntax error, it means the code is not valid Python
        return False

def extract_html_code(body):
    # Parse the HTML content
    soup = BeautifulSoup(chatgpt_db.json_data_to_str(body), 'html.parser')

    # Find all code snippets inside <pre><code> tags
    code_snippets = [pre.get_text() for pre in soup.find_all('pre')]

    # Find all inline code snippets inside <code> tags not within <pre>
    inline_code_snippets = [code.get_text() for code in soup.find_all('code') if code.parent.name != 'pre']  # needs testing, e.g <pre><code>1<code>2</code>3</pre></code>, is it in order?

    # Combine all extracted code snippets
    code = "\n".join(code_snippets)  # + inline_code_snippets) #this relates to the line 78 issue
    # print(extracted_so_api_code)

    return code

def extract_dictionary_code(dictionary):
    code = "\n".join([block["Content"] for block in dictionary])
    return code