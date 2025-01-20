import subprocess, re

def calculate_clone_percentage(simian_output):
    duplicate_lines_line = re.search(r'Found \d+ duplicate lines in \d+ blocks in \d+ files', simian_output)
    print(duplicate_lines_line)
    if not duplicate_lines_line:
        duplicate_lines = 0
    else:
        duplicate_lines = int(re.search(r'\d+', duplicate_lines_line.group()).group())

    total_lines_line = re.search(r'Processed a total of \d+ significant (\d+ raw) lines in \d+ files', simian_output)
    print(total_lines_line)
    if not total_lines_line:
        total_lines = 0
    else:
        total_lines = int(re.search(r'\d+',total_lines_line.group()).group())
    #TODO: choose how to handle the above exceptions

    if total_lines != 0:
        return (duplicate_lines / total_lines) * 100

simian = subprocess.run(
    ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", "../test1.txt", "../test2.txt"],
    text=True, capture_output=True # check=True
)

simian_output = ''.join(simian.stdout.splitlines(keepends=True)[4:-1])
print(simian_output)
print(calculate_clone_percentage(simian_output))
