import os, subprocess, tempfile

code1 = b"""import tempfile
  
f = tempfile.TemporaryFile() 
  
try: 
  f.write(b'Welcome to geeksforgeeks') 
  f.seek(0) 
  data=f.read() 
  print(data) 
finally: 
  f.close()"""
code2 = b"""




import tempfile 
  
f = tempfile.TemporaryFile() 
  
try: 
  f.write(b'Welcome to geeksforgeeks') 
  f.seek(0) 
  data=f.read() 
  print(data) 
finally: 
  f.close()"""

with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code1_file, \
     tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code2_file:

    code1_file.write(code1)
    code2_file.write(code2)

    code1_file.seek(0)
    code2_file.seek(0)

    code1_file.close()
    code2_file.close()

try:
    simian = subprocess.run(
        # ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", "../testcode1.txt", "../testcode2.txt"],
        ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", code1_file.name, code2_file.name],
        text=True, capture_output=True # check=True
    )
    print(simian.stdout)

finally:
    os.remove(code1_file.name)
    os.remove(code2_file.name)