import requests
import re
import dataset
from bs4 import BeautifulSoup
from config import USER_ID, BOT_TOKEN

db = dataset.connect('sqlite:///hitcon_zeroday.db')
zid_table = db['zid']


def bot(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={USER_ID}&parse_mode=Markdown&disable_web_page_preview=1&text={msg}"
    # print(url)
    requests.get(url)


def main():
    page = 0
    done = 0
    try:
        while (not done or page < 5):
            page += 1
            url = f"https://zeroday.hitcon.org/vulnerability/disclosed/page/{page}"
            # print(url)
            r = requests.get(url)
            if r.status_code != 200:
                return
            soup = BeautifulSoup(r.text, "html.parser")
            if len(soup.find_all('h4')) < 0:
                return
            for item in soup.find_all('h4'):
                zid = re.findall("ZD-\d{4}-\d{5}", str(item))[0]
                name = item.string
                if zid_table.find_one(zid=zid) != None:
                    return
                else:
                    zid_table.insert(dict(zid=zid))
                    report_url = f"https://zeroday.hitcon.org/vulnerability/{zid}"
                    # print(report_url)
                    report_content = requests.get(report_url)
                    soup = BeautifulSoup(report_content.text, "html.parser")
                    payload = str(soup.select(".urls")[0])[18:-6]
                    msg = f"[{name}]({report_url})\n```{payload}```"
                    bot(msg)
    except:
        bot("error")


if __name__ == '__main__':
    main()
