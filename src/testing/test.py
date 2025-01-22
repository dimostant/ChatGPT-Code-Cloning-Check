# import subprocess, re
#
# def calculate_clone_percentage(simian_output):
#     duplicate_lines_line = re.search(r'Found \d+ duplicate lines in \d+ blocks in \d+ files', simian_output)
#     print(duplicate_lines_line)
#     if not duplicate_lines_line:
#         duplicate_lines = 0
#     else:
#         duplicate_lines = int(re.search(r'\d+', duplicate_lines_line.group()).group())
#
#     total_lines_line = re.search(r'Processed a total of \d+ significant (\d+ raw) lines in \d+ files', simian_output)
#     print(total_lines_line)
#     if not total_lines_line:
#         total_lines = 0
#     else:
#         total_lines = int(re.search(r'\d+',total_lines_line.group()).group())
#     #TODO: choose how to handle the above exceptions
#
#     if total_lines != 0:
#         return (duplicate_lines / total_lines) * 100
#
# simian = subprocess.run(
#     ["java", "-jar", "../simian-academic/simian-4.0.0/simian-4.0.0.jar", "../test1.txt", "../test2.txt"],
#     text=True, capture_output=True # check=True
# )
#
# simian_output = ''.join(simian.stdout.splitlines(keepends=True)[4:-1])
# print(simian_output)
# print(calculate_clone_percentage(simian_output))

import pandas as pd
import os, time
# numpy as np

os.remove('test.xlsx')
os.popen("copy " + str('testtmp.xlsx') + " " + str('test.xlsx'))

time.sleep(1)
df = pd.read_excel("test.xlsx")

#datas = "I can confirm puppeteer is installed globally but I'm still getting error:\n\nThe command \"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin NODE_PATH=`npm root -g` node '/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/src/../bin/browser.js' '{\"url\":\"https:\\/\\/www.google.com\\/\",\"action\":\"screenshot\",\"options\":{\"type\":\"png\",\"path\":\"example.png\",\"args\":[],\"viewport\":{\"width\":800,\"height\":600}}}'\" failed. Exit Code: 1(General error) Working directory: /home/forge/dev1.rrdevours.monster/public Output: ================ Error Output: ================ \u001b[1m\u001b[43m\u001b[30m Puppeteer old Headless deprecation warning:\u001b[0m\u001b[33m In the near feature `headless: true` will default to the new Headless mode for Chrome instead of the old Headless implementation. For more information, please see https://developer.chrome.com/articles/new-headless/. Consider opting in early by passing `headless: \"new\"` to `puppeteer.launch()` If you encounter any bugs, please report them to https://github.com/puppeteer/puppeteer/issues/new/choose.\u001b[0m Error: Could not find Chrome (ver. 113.0.5672.63). This can occur if either 1. you did not perform an installation before running the script (e.g. `npm install`) or 2. your cache path is incorrectly configured (which is: /home/forge/.cache/puppeteer). For (2), check out our guide on configuring puppeteer at https://pptr.dev/guides/configuration. at ChromeLauncher.resolveExecutablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:300:27) at ChromeLauncher.executablePath (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:181:25) at ChromeLauncher.computeLaunchArguments (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ChromeLauncher.js:97:37) at async ChromeLauncher.launch (/usr/lib/node_modules/puppeteer/node_modules/puppeteer-core/lib/cjs/puppeteer/node/ProductLauncher.js:83:28) at async callChrome (/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/bin/browser.js:84:23)\n\nI suspect this is due to the file path issue you mentioned. Here is output from npm list -g puppeteer and confirmation of install - please provide next steps:\n\n10 packages are looking for funding\n  run `npm fund` for details\nnpm notice \nnpm notice New minor version of npm available! 9.5.1 -> 9.7.1\nnpm notice Changelog: https://github.com/npm/cli/releases/tag/v9.7.1\nnpm notice Run npm install -g npm@9.7.1 to update!\nnpm notice \nforge@aged-dusk:~/dev1.rrdevours.monster$ npm list -g puppeteer\n/usr/lib \n\u2514\u2500\u2500 puppeteer@20.5.0"

print(df.to_string())
df.drop(df.tail(1).index, inplace=True)

print(df.to_string())
cols = df.columns.tolist()

df.loc[len(df)] = ""
df.loc[len(df) - 1] = "I can confirm puppeteer is installed globally but I'm still getting error:\n\nThe command \"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin NODE_PATH=`npm root -g` node '/home/forge/dev1.rrdevours.monster/vendor/spatie/browsershot/src/../bin/browser.js' '{\"url\":\"https:\\/\\/www.google.com\\/\",\"action\":\"screenshot\",\"options\":{\"type\":\"png\",\"path\":\"example.png\",\"args\":[],\"viewport\":{\"width\":800,\"height\":600}}}'\" failed. Exit Code: 1(General error) Working directory: /home/forge/dev1.rrdevours.monster/public Output:  ================ Error Output: ================ \u001b[1m\u001b[43m\u001b[30m Puppeteer old Headless deprecation warning:"

# position = datas.find('\xA4')
# print(position)
# print(datas[position-10:position+10])
#
# df.loc[len(df), 1] = datas

df.to_excel('test.xlsx', index=False)

