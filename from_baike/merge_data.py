#coding=utf-8

import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import chardet

origin_file = "../data/origin_data"
detail_file = "../data/detail_file"
result_file = "../data/result_file.csv"
title_list = [u"同义词",u"中文名",u"英文名",u"简    称",u"创办时间",u"类    别",u"学校类型",u"属    性",u"所属地区",u"学校地址",u"主管部门",u"学校官网",u"学校代码"]

def merge_process(word,organ_dict):
    title_dict = organ_dict.get(word,{})
    value_list = [word]
    for title in title_list:
        value = title_dict.get(title,"")
        value_list.append(value)
    output = "$".join(value_list)
    if len(title_dict) > 100:
        for key,value in title_dict.items():
            print key,value 
        exit(0)
    return output

def run():
    organ_dict = {}
    with open(detail_file) as f:
        for line in f:
            ary = line.strip("\n").split("\001")
            word = ary[0]
            organ_dict[word] = json.loads(ary[1])

    fw = open(result_file,"w")
    with open(origin_file) as f:
        for line in f:
            word = line.strip()
            output = merge_process(word,organ_dict)
            fw.write(output + "\n")
    fw.close()

if __name__ == "__main__":
    run()
