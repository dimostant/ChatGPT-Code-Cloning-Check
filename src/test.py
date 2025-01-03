import os, pandas as pd, numpy as np

so_api_question_id = 0
str_so_api_clean_question = ""
str_gpt_question = ""


df = pd.read_excel(os.path.join('..', 'results.xlsx'))
print(df.to_string())

# df.drop(['Unnamed: 0'], axis = 1, inplace = True)
print(df.to_string())

df_row = len(df.index) - 1

# excel columns
so_qid = 0
so_question_text = 1
mnaist_qindex = 2
mnaist_question_text = 3
question_similarity = 4

# df.iloc[df_row, so_qid]           = so_api_question_id
# df.iloc[df_row, so_question_text] = str_so_api_clean_question
# df.iloc[df_row, mnaist_qindex] = '' # TODO: define chat question index
# df.iloc[df_row, mnaist_question_text] = str_gpt_question

row = [ so_api_question_id, str_so_api_clean_question, ' ', str_gpt_question, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan ]

df.loc[len(df)] = row
df_row += 1

print(df.to_string())

df.to_excel(os.path.join('..', 'results.xlsx'), index=False)