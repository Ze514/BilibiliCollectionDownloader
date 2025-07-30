import requests
import os
import random

desc_api = r"https://api.bilibili.com/x/vas/dlc_act/act/basic"
single_item_api = r"https://api.bilibili.com/x/vas/dlc_act/lottery_home_detail"

def rand_ua():
    with open("uapool.txt", 'r', encoding='utf-8') as f:
        return random.choice(f.readlines()).strip("\n")
def pre_process(data):
    headers = {
        "User-Agent": r"tv.danmaku.bili/7440300 (Linux; U; Android 13; zh_CN; 2312DRAABC; Build/TP1A.220624.014; Cronet/88.0.4324.188)",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    pics = {}
    videos = {}
    cover = set()
    act_id = data['properties']['dlc_act_id']
    lottery_id = data['properties']['dlc_lottery_id']
    semi = requests.get(desc_api, params={'act_id':act_id, 'lottery_id':lottery_id}, headers=headers)
    semi=semi.json()
    introduction = semi['data']['product_introduce']
    path = semi['data']['act_title']
    cover.add(requests.get(desc_api, params={'act_id':act_id, 'lottery_id':lottery_id}, headers=headers).json()['data']['act_y_img'])
    resp = requests.get(single_item_api, params={'act_id':act_id, 'lottery_id':lottery_id}, headers=headers)
    resp = resp.json()['data']
    for item in resp['item_list']:
        pics.setdefault(item['card_info']['card_name'], item['card_info']['card_img'])
        if item['card_info']['video_list'] is not None:
            sort_sense = 0
            for video in item['card_info']['video_list']:
                videos.setdefault(item['card_info']['card_name']+str(sort_sense),video)
                sort_sense += 1
    return (pics, videos, introduction, cover, path)
    
def download(pics: dict, videos: dict, introduction, cover: set, path):
    headers = {
        "User-Agent": rand_ua(),
    }
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "INTRODUCTION.txt"),'w',encoding='utf-8') as file:
        file.write(introduction)
    if len(pics) != 0:
        for key, value in pics.items():
            resp = requests.get(value, headers=headers)
            with open(os.path.join(path, key+".webp"), 'wb') as f:
                f.write(resp.content)
            print(f"{key}.webp saved")
    if len(videos) != 0:
        for key, value in videos.items():
            resp = requests.get(value, headers=headers)
            with open(os.path.join(path, key+".mp4"), 'wb') as f:
                f.write(resp.content)
            print(f"{key}.mp4 saved")
            break
    if len(cover) != 0:
        resp = requests.get(cover.pop(), headers=headers)
        with open(os.path.join(path, "cover.webp"), 'wb') as f:
            f.write(resp.content)
            print("cover saved")
    


def main(data):
    middle = pre_process(data) 
    download(*middle)
