import pandas as pd
import os, time

from src.ChatGBT_db.devgpt_chats import get_json_data, get_user_conversation, get_conversation_question, json_data_to_str
# numpy as np
from src.code_handling import remove_ansi_escape_sequences, remove_non_utf8_chars

os.remove('test.xlsx')
os.popen("copy " + str('testtmp.xlsx') + " " + str('test.xlsx'))

time.sleep(1)
df = pd.read_excel("test.xlsx")

#datas = "I can confirm puppeteer is installed globally but I'm still getting error:\n\nThe command \"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin NODE_PATH=`npm root -g` node '/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/src/../bin/browser.js' '{\"url\":\"https:\\/\\/www.google.com\\/\",\"action\":\"screenshot\",\"options\":{\"type\":\"png\",\"path\":\"example.png\",\"args\":[],\"viewport\":{\"width\":800,\"height\":600}}}'\" failed. Exit Code: 1(General error) Working directory: /home/forge/dev1.rrdevours.monster/public Output: ================ Error Output: ================ \u001b[1m\u001b[43m\u001b[30m Puppeteer old Headless deprecation warning:\u001b[0m\u001b[33m In the near feature `headless: true` will default to the new Headless mode for Chrome instead of the old Headless implementation. For more information, please see https://developer.chrome.com/articles/new-headless/. Consider opting in early by passing `headless: \"new\"` to `puppeteer.launch()` If you encounter any bugs, please report them to https://github.com/puppeteer/puppeteer/issues/new/choose.\u001b[0m Error: Could not find Chrome (ver. 113.0.5672.63). This can occur if either 1. you did not perform an installation before running the script (e.g. `npm install`) or 2. your cache path is incorrectly configured (which is: /home/forge/.cache/puppeteer). For (2), check out our guide on configuring puppeteer at https://pptr.dev/guides/configuration. at ChromeLauncher.resolveExecutablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:300:27) at ChromeLauncher.executablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:181:25) at ChromeLauncher.computeLaunchArguments (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:97:37) at async ChromeLauncher.launch (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:83:28) at async callChrome (/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/bin/browser.js:84:23)\n\nI suspect this is due to the file path issue you mentioned. Here is output from npm list -g puppeteer and confirmation of install - please provide next steps:\n\n10 packages are looking for funding\n  run `npm fund` for details\nnpm notice \nnpm notice New minor version of npm available! 9.5.1 -> 9.7.1\nnpm notice Changelog: https://github.com/npm/cli/releases/tag/v9.7.1\nnpm notice Run npm install -g npm@9.7.1 to update!\nnpm notice \nforge@aged-dusk:~/dev1.rrdevours.monster$ npm list -g puppeteer\n/usr/lib \n\u2514\u2500\u2500 puppeteer@20.5.0"

print(df.to_string())
df.drop(df.tail(1).index, inplace=True)

print(df.to_string())
cols = df.columns.tolist()
#df['B'] = 2
df.loc[len(df)] = ""

# text = "I can confirm puppeteer is installed globally but I'm still getting error: \
# \
# The command "PATH=$PATH:/usr/local/bin:/opt/homebrew/bin NODE_PATH=`npm root -g` node '/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/src/../bin/browser.js' '{"url":"https:\/\/www.google.com\/","action":"screenshot","options":{"type":"png","path":"example.png","args":[],"viewport":{"width":800,"height":600}}}'" failed. Exit Code: 1(General error) Working directory: /home/forge/dev1.rrdevours.monster/public Output: ================ Error Output: ================  Puppeteer old Headless deprecation warning: In the near feature `headless: true` will default to the new Headless mode for Chrome instead of the old Headless implementation. For more information, please see https://developer.chrome.com/articles/new-headless/. Consider opting in early by passing `headless: "new"` to `puppeteer.launch()` If you encounter any bugs, please report them to https://github.com/puppeteer/puppeteer/issues/new/choose. Error: Could not find Chrome (ver. 113.0.5672.63). This can occur if either 1. you did not perform an installation before running the script (e.g. `npm install`) or 2. your cache path is incorrectly configured (which is: /home/forge/.cache/puppeteer). For (2), check out our guide on configuring puppeteer at https://pptr.dev/guides/configuration. at ChromeLauncher.resolveExecutablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:300:27) at ChromeLauncher.executablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:181:25) at ChromeLauncher.computeLaunchArguments (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:97:37) at async ChromeLauncher.launch (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:83:28) at async callChrome (/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/bin/browser.js:84:23)  \
#  \
# I suspect this is due to the file path issue you mentioned. Here is output from npm list -g puppeteer and confirmation of install - please provide next steps: \
#  \
# 10 packages are looking for funding \
#   run `npm fund` for details \
# npm notice \
# npm notice New minor version of npm available! 9.5.1 -> 9.7.1 \
# npm notice Changelog: https://github.com/npm/cli/releases/tag/v9.7.1 \
# npm notice Run npm install -g npm@9.7.1 to update! \
# npm notice \
# forge@aged-dusk:~/dev1.rrdevours.monster$ npm list -g puppeteer \
# /usr/lib \
#  puppeteer@20.5.0" cannot be used in worksheets."

dev_gpt_json = get_json_data(
    '../ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'
)

text = get_conversation_question( get_user_conversation(dev_gpt_json, 10, 0, 3) )
#print(text)
str_text = json_data_to_str(text)
clean_text = remove_non_utf8_chars(str_text)
clean_text = remove_ansi_escape_sequences(clean_text)
df.loc[len(df) - 1] = clean_text
# df.loc[len(df) - 1] = ["ONNX", 2]


# position = datas.find('\xA4')
# print(position)
# print(datas[position-10:position+10])
#
# df.loc[len(df), 1] = datas

df.to_excel('test.xlsx', index=False)

