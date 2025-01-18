import subprocess, tempfile, os

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

    finally:
        os.remove(code1_file.name)
        os.remove(code2_file.name)

    return simian.stdout # .strip()

    #convert simian results to percentage