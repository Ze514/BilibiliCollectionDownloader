import requests
import re
import time
import random as rad
import os
import urllib.request
import requests
if os.path.exists("D:\\btio\\collection") is False:
    os.mkdir("D:\\btio\\collection")
savepath = "D:\\btio\\collection"
ua_file = open('.\\uapool.txt', 'r')
ua_lines = ua_file.readlines()
ua = rad.choice(ua_lines)
ua = ua[:-1]
print(ua,"\n")
headers = {
    'User-Agent': ua,
    'Accept-Charset': 'UTF-8'
}
def get_pic(ori):
    container = []
    videocontainer = []
    if type(ori) is str:
        url = ori
        txtid = re.findall(r"act_id=(.*?)&",ori)
        for item in txtid:
            txtid1 = item
        txt_url = f"https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={txtid1}"
    elif type(ori) is list:
        actid = int(ori[0])
        lotteryid = int(ori[1])
        url = f"https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id={actid}&lottery_id={lotteryid}"
        txt_url = f"https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={actid}"
    else:
        url = f"https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id={ori}&lottery_id={ori+1}"
        txt_url = f"https://api.bilibili.com/x/vas/dlc_act/act/basic?act_id={ori}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        txt_resp = requests.get(txt_url, headers=headers, timeout=10)
        if response.status_code == 200 and txt_resp.status_code == 200:
            data = response.json()
            txtdata = txt_resp.json()
            temp = data['data']['item_list']
            foldername = txtdata['data']['act_title']+"["+data['data']['name']+"_"+str(data['data']['lottery_id'])+"]"
            introduction = txtdata['data']['product_introduce']
            cover_pic = txtdata['data']['act_y_img']
            for item in temp:
                picinfo = {
                    'name':item['card_info']['card_name'],
                    'aim':item['card_info']['card_img']
                }
                try:
                    temp_aim = item['card_info']['video_list']
                    temp_aim = temp_aim[0]
                    videoinfo = {
                        'name':item['card_info']['card_name'],
                        'aim':temp_aim
                    }
                    videocontainer.append(videoinfo)
                except TypeError:
                    time.sleep(0.00721)
                container.append(picinfo)
            for hidden_item in data['data']['collect_list']['collect_infos']:
                if hidden_item['card_item'] is not None and hidden_item['effective_forever'] != 0:
                    picinfo = {
                        'name':hidden_item['redeem_item_name'],
                        'aim':hidden_item['redeem_item_image']
                    }
                    container.append(picinfo)
    except TypeError:
        print("非连续，尝试手动档")
        return (0,0,0,0,0)
    except KeyError:
        cover_pic = txtdata['data']['act_y_img']
    except requests.RequestException as e:
        print(e)
        return (0,0,0,0,0)
    return (container,foldername,introduction,cover_pic,videocontainer)
def download(url_obj,folder,txtcontent,cover,video):
    count = 0
    saved_path = os.path.join(savepath+"\\"+folder)
    try:
        os.mkdir(saved_path)
    except FileExistsError:
        print("重复")
        decision = input("覆盖(1)?:")
        if decision == "1":
            print("")
        else:
            return ""
    with open(saved_path+"\\"+"INTRODUCTION.txt",'w',encoding='utf-8') as file:
        file.write(txtcontent)
    urllib.request.urlretrieve(cover,saved_path+"\\"+"cover.png")
    count = 0
    for i in url_obj:
        filename = i['name']
        address = i['aim']
        picresponse = requests.get(address,headers=headers,stream=True)
        if picresponse.status_code == 200:
            count+=1
            with open(saved_path+"\\"+filename+".png",'wb') as fi:
                for picchunk in picresponse.iter_content(8192):
                    fi.write(picchunk)
                print(f"picture part:{count}/{len(url_obj)}")
        time.sleep(0.2)
    if len(video) == 0:
        return 0
    else:
        con = 0
        for videoobj in video:
            name = videoobj['name']
            addre = videoobj['aim']
            response = requests.get(addre,headers=headers,stream=True)
            if response.status_code == 200:
                con+=1
                with open(saved_path+"\\"+name+".mp4",'wb') as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                    print(f"video part:{con}/{len(video)}")
            else:
                print("err")
            time.sleep(0.15)
    return 0
def main(iscalled,externallink):
    if iscalled == True:
        externallist = []
        externallink=externallink+"q"
        actid = "".join(re.findall(r"act_id=(.*?)&",externallink))
        lotteryid = "".join(re.findall(r"lottery_id=(.*?)q",externallink))
        externallist.append(actid)
        externallist.append(lotteryid)
        externaltuple = get_pic(externallist)
        download(*externaltuple)
        return ""
    else:
        link = str(input("URL INPUT(enter m to switch to manual download mode):"))
        if link == "m":
            mainuserinput = int(input("main manual input:"))
            subuserinput = int(input("sub manual input:"))
            newlink = f"https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail?act_id={mainuserinput}&lottery_id={subuserinput}"
            temp_tuple_alt = get_pic(newlink)
            download(*temp_tuple_alt)
            return 1
        elif link == "":
            return 1
        elif link == "e":
            return 0
        else:
            processedlink = re.findall(r"html\?id=(.*?)&",link)
            if len(processedlink) == 0:
                processedlink = re.findall(r"act_id=(.*?)&",link)
            for link_obj in processedlink:
                temp_tuple = get_pic(int(link_obj))
            if temp_tuple == (0,0,0,0,0):
                return 1
            else:
                download(*temp_tuple)
                return 1
if __name__ == "__main__":
    keep = True
    while keep:
        result = main(False,"")
        if result == 0:
            keep = False
        else:
            time.sleep(0.01)
        