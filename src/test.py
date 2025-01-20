# import subprocess, tempfile
import os
import pandas as pd, numpy as np
#
#
# # with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code1_file, \
# #      tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as code2_file:
# #
# #     code1_file.write(gpt_answer_code.encode('ascii'))
# #     code2_file.write(so_api_answer_code.encode('ascii'))
# #
# #     code1_file.seek(0)
# #     code2_file.seek(0)
# #
# #     code1_file.close()
# #     code2_file.close()
# #
# # try:
# simian = subprocess.run(
#     ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", "../test1.txt", "../test2.txt"],
#     text=True, capture_output=True # check=True
# )
#
# # print(simian.stdout)
# print(''.join(simian.stdout.splitlines(keepends=True)[4:-2]))
#
# # finally:
# #     os.remove(code1_file.name)
# #     os.remove(code2_file.name)
# #
# # return simian.stdout #

df = pd.read_excel(os.path.join('..', 'results.xlsx'))
df.loc[len(df)] = [
    1, 2, 3, 4, 5, np.nan, np.nan, 8, np.nan, np.nan
]
df.to_excel(os.path.join('..', 'results.xlsx'), index=False)


xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
column_names = xl.columns.tolist()
# xl.loc[len(xl) - 1 if len(xl) > 0 else len(xl)] = [
#     np.nan, np.nan, np.nan, np.nan, np.nan, 6, 7, np.nan, 9, 10
# ]
xl.loc[len(xl) - 1 if len(xl) > 0 else len(xl), [column_names[5], column_names[6], column_names[8], column_names[9]]] = [6, 7, 9, 10]
xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)