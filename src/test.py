import subprocess, tempfile

code1 = b"print('1')"
code2 = b"print('1')"

code1_file = tempfile.TemporaryFile()
code2_file = tempfile.TemporaryFile()

try:
    code1_file.write(code1)
    code1_file.seek(0)

    print(code1_file.read())

    code2_file.write(code2)
    code2_file.seek(0)

    print(code2_file.read())

    # simian = subprocess.run(
    #     ["java", "-jar", "/simian-academic/simian-4.0.0/simian-4.0.0.jar", code1_file.read(), code2_file.read()],
    #     check=True, text=True, capture_output=True
    # )
    # print(simian.stdout)
    simian = subprocess.run(
        ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", "../testcode1", "../testcode1"],
        check=True, text=True, capture_output=True
    )
    print(simian.stdout)

finally:
    code1_file.close()
    code2_file.close()


