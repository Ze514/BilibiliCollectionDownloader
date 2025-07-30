import requests
import new_download
headers = {
    "User-Agent": "tv.danmaku.bili/7440300 (Linux; U; Android 13; zh_CN; 2312DRAABC; Build/TP1A.220624.014; Cronet/88.0.4324.188)"
}
def quick_get_for_loop(kw,pn):
    baseurl = r"https://api.bilibili.com/x/garb/v2/mall/home/search"
    params = {
        'key_word': kw,
        'ps': 10,
        'pn': pn
    }
    response = requests.get(baseurl, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        echo(data)
        usr_decision = input("是否继续？(y/c/(number)/n(ew))")
        if usr_decision == 'y':
            return 1
        elif usr_decision == 'c':
            return 0
        elif usr_decision == 'n':
            return 2
        else:
            return data['data']['list'][int(usr_decision)-1]

def echo(data):

    next_counter = 0
    for item in data['data']['list']:
        if item['part_id'] == 0:
            itstype = "收藏集"
            next_counter += 1
        else:
            itstype = "装扮"
            next_counter += 1
        print("--------------------")
        print("序号："+str(next_counter)+"\n")
        print("名称："+item['name']+"\n",
                "类型："+itstype+"\n")    



def main():
    search = str(input("键入搜索词："))
    while search == "":
        search = str(input("键入搜索词："))
    quick_get_for_loop(search,1)
    usr_decision_counter = 1
    while search != "c":
        value = quick_get_for_loop(search,usr_decision_counter)
        
        if value == 1:
            usr_decision_counter += 1
            quick_get_for_loop(search, usr_decision_counter)
        elif value == 0:
            break
        elif value == 2:
            search = str(input("键入搜索词："))
        else:
            new_download.main(value)
if __name__ == "__main__":
    main()