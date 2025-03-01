import os
import time
import requests
import re
headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79",
    'Accept-Charset':"UTF-8"
    }
def main(keyword,pn):
    searchpage = f'https://api.bilibili.com/x/garb/v2/mall/home/search?pn={pn}&key_word=\"'+keyword+"\""
    searchdata_raw = requests.get(searchpage,headers=headers)
    serachdata = searchdata_raw.json()
    num = 0
    for i in serachdata['data']['list']:
        if i['properties']['type'] == "ip":
            print(num,i['name'],"装扮",sep="   ")
        else:
            print(num,i['name'],"收藏集",sep="   ")
        num += 1
    usr_choice = input("有无？：")
    if usr_choice == "":
        return 1
    elif usr_choice == "e":
        return 2
    else:
        download(serachdata['data']['list'][int(usr_choice)])
        return 0
def download(url):
    if url['properties']['type'] == "ip":
        ipclass(url['item_id'])
    elif url['properties']['type'] == "dlc_act":
        dlcclass(url['jump_link'])
    return 0
def ipclass(ipaim):
    ipapi = f"https://api.bilibili.com/x/garb/v2/user/suit/benefit?item_id={ipaim}&part=cards"
    ip_raw = requests.get(ipapi,headers=headers)
    ipinfo = ip_raw.json()
    time.sleep(0.1)
    foldername = ipinfo['data']['name']
    text = ipinfo['data']['properties']['desc']
    if os.path.exists(f".\\{foldername}") is False:
        downloadexpert(0,0,foldername,foldername)

    else:
        time.sleep(0.01)
    with open(f".\\{foldername}\\"+"INTRODUCTION.TXT",'w',encoding="UTF-8") as desc:
        desc.write(text)
    try:
        for cardobj in ipinfo['data']['suit_items']['card']:
            cardname = cardobj['name']
            cardurl = cardobj['properties']['image']
            downloadexpert(cardurl,"card",cardname,foldername)
        for card_bgobj in ipinfo['data']['suit_items']['card_bg']:
            downloadexpert(card_bgobj['properties']['image'],"card_bg",card_bgobj['name'],foldername)
        for emojiobj in ipinfo['data']['suit_items']['emoji_package'][0]['items']:
            downloadexpert(emojiobj['properties']['image'],"emoji_package",emojiobj['name'],foldername)
        for skinobj in ipinfo['data']['suit_items']['skin']:
            downloadexpert(skinobj['properties']['head_bg'],"skin",skinobj['name'],foldername)
        for spacebgobj in ipinfo['data']['suit_items']['space_bg']:
            downloadexpert(spacebgobj['properties']['image1_protrait'],"space_bg",spacebgobj['name'],foldername)
    except KeyError:
        time.sleep(0.1)
    return 0
def downloadexpert(url,savepath,filename,folder):
    if url == 0 and savepath == 0 and os.path.exists(f".\\{filename}") is False:
        foldername = filename
        os.mkdir(f".\\{foldername}")
    else:
        if os.path.exists(f".\\{folder}\\{savepath}") is False:
            os.mkdir(f".\\{folder}\\{savepath}")
        resp = requests.get(url,timeout=10,headers=headers,stream=True)
        if resp.status_code == 200:
            with open(f".\\{folder}\\{savepath}\\{filename}.webp",'wb') as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
    return 0
def dlcclass(dlcaim):
    dlcaim = dlcaim + "EOL"
    actid=re.findall(r"act_id=(.*?)&",dlcaim)[0]
    lotteryid = re.findall(r"lottery_id=(.*?)EOL",dlcaim)[0]
    txt_url = f"https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={actid}"
    url = f"https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id={actid}&lottery_id={lotteryid}"
    txt_resp = requests.get(txt_url,headers=headers)
    txt_json = txt_resp.json()
    resp = requests.get(url,headers=headers)
    de_resp = resp.json()
    foldername = txt_json['data']['act_title']+"["+de_resp['data']['name']+"_"+str(de_resp['data']['lottery_id'])+"]"
    txt = txt_json['data']['product_introduce']
    if os.path.exists(f".\\{foldername}") is False:
        os.mkdir(f".\\{foldername}")
    else:
        time.sleep(0.001)
    with open(f".\\{foldername}\\INTRODUCTION.TXT",'w') as txtfile:
        txtfile.write(txt)
    temp = de_resp['data']['item_list']
    cover_pic = txt_json['data']['act_y_img']
    cover_resp = requests.get(cover_pic,headers=headers,stream=True)
    with open(f".\\{foldername}\\cover.png",'wb') as coverpic:
        for chunk in cover_resp.iter_content(8192):
            coverpic.write(chunk)
    for i in temp:
        picinfo = {
            'name':i['card_info']['card_name'],
            'aim':i['card_info']['card_img']
            }
        pic = requests.get(i['card_info']['card_img'],headers=headers,stream=True)
        with open(f".\\{foldername}\\{i['card_info']['card_name']}"+".webp",'wb') as spic:
            for chunk in pic.iter_content(8192):
                spic.write(chunk)
        try:
            videoaim = i['card_info']['video_list'][0]
            videoname = i['card_info']['card_name']
            video_resp = requests.get(videoaim,headers=headers,stream=True)
            with open(f".\\{foldername}\\{videoname}"+".mp4",'wb') as video:
                for chunk in video_resp.iter_content(8192):
                    video.write(chunk)
            for hidden_item in de_resp['data']['collect_list']['collect_infos']:
                if hidden_item['card_item'] is not None and hidden_item['effective_forever'] != 0:
                    hiddenresp = requests.get(hidden_item['redeem_item_image'],headers=headers,stream=True)
                    with open(f".\\{foldername}\\{hidden_item['redeem_item_name']}"+".webp","wb") as hiddenobj:
                        for chunk in hiddenresp.iter_content(8192):
                            hiddenobj.write(chunk)
        except TypeError:
            print("no video")
    return 0
status = True
while status:
    count = 1
    searchwords = input("搜索：")
    while searchwords != "e":
        rtval = main(searchwords,count)
        if rtval == 1:
            count += 1
        else:
            break
    status = False