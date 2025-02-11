import requests
import os
import urllib.error,urllib.request
import re
import time
import megapx
headers = {
    'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 13; 2312DRAABC Build/TP1A.220624.014)',
    'Accept-Charset':'UTF-8'
}
def query(keyword,pn):
    url = f'https://api.bilibili.com/x/garb/v2/mall/home/search?pn={pn}&key_word=\"'+keyword+"\""
    pagedata = requests.get(url,headers=headers,timeout=15)
    if pagedata.status_code == 200:
        result = pagedata.json()
        time.sleep(0.0721)
        single_page_end = len(result['data']['list'])
        all_page_end = ((result['data']['total'] // 10)+1)
        count = 0
        all_page_count = 0
        print(all_page_end)
        while count != single_page_end:
            print(count,result['data']['list'][count]['name']+"\n",sep="    ")
            count += 1
        shotedcheck = str(input("有无？："))
        if shotedcheck == '':
            all_page_count += 1
            return 0
        elif shotedcheck == "e":
            return 1
        else:
            return result['data']['list'][int(shotedcheck)]['jump_link']
def nextpage(isnextpage):
    if isnextpage is True:
        query()
def main():
    search = str(input("键入搜索词："))
    while search == "":
        search = str(input("键入搜索词："))
#    page = int(input("键入页数："))
    count = 1
    while search != "e":
        tempresult = query(search,count)
        if tempresult == 0:
            count +=1
#            query(search,count)
        elif tempresult == 1:
            break
        else:
            matobj=re.match(r"(.*?)/suit/(.*?)",tempresult)
            if matobj is not None:
                tempresult=query(search,count)
                megapx.main(True,tempresult)
                return ""
            else:
                megapx.main(True,tempresult)
                return ""
    return ""
main()