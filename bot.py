import requests
import sys
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

user_id = 'user_id'
bot_token = 'bot_token'
log_path = './bot.log'

with open(log_path, 'r') as f:
    log = f.readlines()

first = 0
if len(log) == 0:
    first = 1
else:
    last = log[-1][:-1]
page = 0
done = 0
catch = []
while not done:
    page += 1
    url = "https://zeroday.hitcon.org/vulnerability/disclosed/page/" + str(page)

    r = requests.get(url)
    if r.status_code != 200:
        sys.exit(1)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.find_all('h4'):
        zid = re.findall("ZD-\d{4}-\d{5}", str(item))[0]
        name = item.string
        if first:
            catch.append(zid)
            done = 1
            break
        if zid == last:
            done = 1
            break
        else:
            catch.append(zid)
            msg = "[" + name + "](https://zeroday.hitcon.org/vulnerability/" + zid + ")"
            url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + user_id + "&parse_mode=Markdown&disable_web_page_preview=1&text=" + msg
            print(url)
            requests.get(url)
with open(log_path, 'a') as f:
    for item in reversed(catch):
        f.write(item + "\n")
