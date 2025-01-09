import subprocess

def code_cloning_check(gpt_answer_code, so_api_answer_code):
    print("\ncomparing answers :\n", gpt_answer_code.replace("\n", " "), "\nand :\n", so_api_answer_code.replace("\n", " "))
    # insert code to abstract syntax tree (python code only!)??
    # tree1 = ast.parse(extracted_so_api_code)
    # tree2 = ast.parse(gpt_answer_clean_code)

    simian = subprocess.run(["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar"], check=True, capture_output=True)
    # subprocess.run(["java", "-jar", "/simian-academic/simian-4.0.0/simian-4.0.0.jar"], check=True, capture_output=True)

    print("cloning or not cloning idk lmao!!!!...")