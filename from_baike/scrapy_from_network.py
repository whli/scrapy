#coding=utf-8

import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup as sp
import json
import re


url_head = "https://baike.baidu.com/item/"

header = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
pattern_name = r".*?<span class=\"viewTip-fromTitle\">(.*?)</span>.*?"
pattern_title = r"<dt class=\"basicInfo-item name\">(.*?)</dt>"
pattern_value = r"<dd class=\"basicInfo-item value\">\n(.*?)\n</dd>"
p_2 = r".*?target=\"_blank\">(.*?)</a>.*?"
p_3 = r"<dd class=\"basicInfo-item value\">\n(.*?)\n"


def get_detail(word):
    value_dict = {}
    url = url_head + word
    req = Request(url, headers=header)
    html = urllib2.urlopen(req).read()
    soup = sp(html,"html.parser")
    list_same = re.findall(pattern_name,html)
    if list_same:
        value_dict["同义词"] = list_same[0]
    list_title = soup.find_all("dt", class_="basicInfo-item name")
    list_value = soup.find_all("dd", class_="basicInfo-item value")
    for index,item in enumerate(list_title):
        title = re.findall(pattern_title,str(item))[0]
        value_list = re.findall(pattern_value,str(list_value[index]))
        if value_list and value_list[0].find("target") <= 0:
            value_dict[title] = value_list[0]
            continue
        elif value_list and value_list[0].find("target") > 0:
            value = re.findall(p_2,str(value_list[0]))
            if value:
                value_dict[title] = value[0]
                continue

        value_list = re.findall(p_2,str(list_value[index]))
        if value_list:
            value = ""
            for item in value_list:
                value += item + ";"
            value = value.strip(";")
            value_dict[title] = value
            continue

        value_list = re.findall(p_3,str(list_value[index]))
        if value_list:
            value_dict[title] = value_list[0]
            continue

    if 0:
        for key,value in value_dict.items():
            print key,value
    return word + "\001" + json.dumps(value_dict)

def run(filename):
    detail_file = "../data/detail_file"
    fw = open(detail_file,"w")
    with open(filename) as f:
        for line in f:
            word = line.strip()
            detail_info = get_detail(word)
            fw.write(detail_info + "\n")
    fw.close()

if __name__ == "__main__":
    tar_file = "../data/organ"  # organ \ test
    run(tar_file)
