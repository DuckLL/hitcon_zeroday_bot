import requests
import sys
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

user_id = 'user_id'
bot_token = 'bot_token'
log_path = './bot.log'
max_send = 20

try:
    f = open(log_path, 'r')
    log = f.readlines()
    last = log[-1][:-1]
except:
    f = open(log_path, 'w')
    last = ""
finally:
    f.close()

page = 0
done = 0
catch = []
while not done:
    page += 1
    url = "https://zeroday.hitcon.org/vulnerability/disclosed/page/" + str(page)
    # print(url)
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit(1)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.find_all('h4'):
        zid = re.findall("ZD-\d{4}-\d{5}", str(item))[0]
        name = item.string
        if zid == last or len(catch) > max_send:
            done = 1
            break
        else:
            catch.append(zid)
            report_url = "https://zeroday.hitcon.org/vulnerability/" + zid
            # print(report_url)
            report_content = requests.get(report_url)
            soup = BeautifulSoup(report_content.text, "html.parser")
            payload = str(soup.select(".urls")[0])[18:-6]
            msg = "[" + name + "](" + report_url + ") ```" + payload + "```"
            url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + user_id + "&parse_mode=Markdown&disable_web_page_preview=1&text=" + msg
            requests.get(url)
with open(log_path, 'a') as f:
    for item in reversed(catch):
        f.write(item + "\n")
