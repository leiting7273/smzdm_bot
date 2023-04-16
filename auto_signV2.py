# coding:utf-8

import hashlib
import operator
import random
import time
import requests

key = 'apr1$AwP!wRRT$gJ/q.X24poeBInlUJC'
user_tuple = (
    {
        'sk': 'HWz4OZDUNASn+/Z3OqdkRQAiclWXJaAfW+0UOE/ROgu34Qezct6cxQI3vFwfJsln',
        'token': 'BB-hFldh/2fV1Xpz4aGSVyDYKNQ485xlYHPFj+gzznnBk8/jZraMmYCGxtSCln7j3RoRaVjU1s3fnC43EjVHl0cXVuIEFo=',
        'cookie': 'smzdm_version=10.4.40;device_type=XiaomiMi-4c;client_id=05018a2f057aa1474d938d08937599ae.1681390298540;rs_id2=;apk_partner_name=smzdm_wap;last_article_info=;oaid=;rs_id4=;imei=;register_time=1484800684;login=1;smzdm_id=5336577653;session_id=05018a2f057aa1474d938d08937599ae.1681391520250;partner_name=smzdm_wap;device_recfeed_setting=%7B%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D;is_new_user=0;android_id=bcb03b6d519005c3b298650af9b85e60;partner_id=165;apk_partner_id=165;rs_id3=;rs_id1=;pid=j2TWcApUVogBiOeqmDIA5vApMapF66YoiwRIkQGK605zbfQDpoHn1A%3D%3D;sess=BB-hFldh%2F2fV1Xpz4aGSVyDYKNQ485xlYHPFj%2BgzznnBk8%2FjZraMmYCGxtSCln7j3RoRaVjU1s3fnC43EjVHl0cXVuIEFo%3D;longitude=960c836c68ce48d4;device_smzdm_version_code=880;new_device_id=bcb03b6d519005c3b298650af9b85e60;rs_id5=;network=1;device_system_version=5.1.1;device_id=05018a2f057aa1474d938d08937599ae;device_push=1;sessionID=05018a2f057aa1474d938d08937599ae.1681391520250;device_smzdm=android;active_time=1681391522;basic_v=0;latitude=960c836c68ce48d4;device_s=bcb03b6d519005c3b298650af9b85e60;device_smzdm_version=10.4.40;ab_test=c;',
    },
)


def md5(m: str) -> str:
    return hashlib.md5(m.encode()).hexdigest()


def dict_to_query(a: list) -> str:
    query_str = ''
    for k, v in a:
        query_str += f"{k}={v}&"
    return query_str[:-1]


def get_sign(src: dict) -> str:
    data = src.copy()
    if 'sign' in data:
        del data['sign']

    # del key if value is ''
    for k in list(data.keys()):
        if not data[k]:
            del data[k]

    sorted_data = sorted(data.items(), key=operator.itemgetter(0))
    m = dict_to_query(sorted_data) + f'&key={key}'
    return md5(m).upper()


def get_headers_and_timestamp_wrapper():
    timestamp = (int(time.time()) - random.randint(10, 20)) * 1000

    def get_headers_and_timestamp(cookie: str):
        headers = {
            'User-Agent': 'smzdm_android_V10.4.40 rv:880 (Mi-4c;Android5.1.1;zh)smzdmapp',
            'request_key': str(
                random.randint(10000000, 100000000) * 10000000000 + int(time.time())
            ),
            'Host': 'user-api.smzdm.com',
            'Cookie': cookie,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        return headers, timestamp

    return get_headers_and_timestamp


get_headers_and_timestamp = get_headers_and_timestamp_wrapper()


def checkin(sk: str, token: str, cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin'
    headers, timestamp = get_headers_and_timestamp(cookie)
    timestamp = int(time.time())
    data = {
        'weixin': '1',
        'captcha': '',
        'f': 'android',
        'v': '10.4.40',
        'sk': sk,
        'touchstone_event': '',
        'time': timestamp,
        'token': token,
        'basic_v': '0',
    }
    data['sign'] = get_sign(data)
    res = requests.post(url, headers=headers, data=data).json()
    print('checkin --->', res)
    if res['error_code'] != '0':
        raise Exception(res['error_msg'])

    if '成功' in res['error_msg']:
        return True
    else:
        return False


def reward(url: str, cookie: str) -> bool:
    headers, timestamp = get_headers_and_timestamp(cookie)
    data = {
        'weixin': '1',
        'time': timestamp,
        'basic_v': '0',
        'f': 'android',
        'v': '10.4.40',
    }
    data['sign'] = get_sign(data)
    res = requests.post(url, headers=headers, data=data).json()
    print(url.split('/')[-1], '--->', res)

    if res['error_code'] == '0':
        return True
    if res['error_code'] == '4':
        return False
    else:
        raise Exception(res['error_msg'])


def all_reward(cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin/all_reward'
    return reward(url, cookie)


def extra_reward(cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin/extra_reward'
    return reward(url, cookie)


for user in user_tuple:
    try:
        print(checkin(**user))
    except:
        pass
    try:
        print(all_reward(user['cookie']))
    except:
        pass
    try:
        print(extra_reward(user['cookie']))
    except:
        pass

# 把值得买的cookie放入下面的单引号里面  有几个帐号就弄几个（默认设置了3个 根据自己情况改）
cookie_list = ['smzdm_version=10.4.40;device_type=XiaomiMi-4c;client_id=05018a2f057aa1474d938d08937599ae.1681390298540;rs_id2=;apk_partner_name=smzdm_wap;last_article_info=;oaid=;rs_id4=;imei=;register_time=1484800684;login=1;smzdm_id=5336577653;session_id=05018a2f057aa1474d938d08937599ae.1681391520250;partner_name=smzdm_wap;device_recfeed_setting=%7B%22haojia_recfeed_switch%22%3A%221%22%2C%22homepage_sort_switch%22%3A%221%22%2C%22other_recfeed_switch%22%3A%221%22%2C%22shequ_recfeed_switch%22%3A%221%22%7D;is_new_user=0;android_id=bcb03b6d519005c3b298650af9b85e60;partner_id=165;apk_partner_id=165;rs_id3=;rs_id1=;pid=j2TWcApUVogBiOeqmDIA5vApMapF66YoiwRIkQGK605zbfQDpoHn1A%3D%3D;sess=BB-hFldh%2F2fV1Xpz4aGSVyDYKNQ485xlYHPFj%2BgzznnBk8%2FjZraMmYCGxtSCln7j3RoRaVjU1s3fnC43EjVHl0cXVuIEFo%3D;longitude=960c836c68ce48d4;device_smzdm_version_code=880;new_device_id=bcb03b6d519005c3b298650af9b85e60;rs_id5=;network=1;device_system_version=5.1.1;device_id=05018a2f057aa1474d938d08937599ae;device_push=1;sessionID=05018a2f057aa1474d938d08937599ae.1681391520250;device_smzdm=android;active_time=1681391522;basic_v=0;latitude=960c836c68ce48d4;device_s=bcb03b6d519005c3b298650af9b85e60;device_smzdm_version=10.4.40;ab_test=c;']
# 活动id
active_id = ['ljX8qVlEA7','er2g3aeEAK']

def getActiveId():
    url = "https://m.smzdm.com/zhuanti/life/choujiang/"
    resp = requests.get(url)
    try:
        re.findall('class="chance-surplus".*?(\d)', resp.text)[0]
    except IndexError:
        # print("No lottery chance left")
        pass
    try:
        lottery_activity_id = re.findall(
            'name="lottery_activity_id" value="(.*?)"', resp.text
        )[0]
    except Exception:
        lottery_activity_id = "A6X1veWE2O"
    return lottery_activity_id

active_id.append(getActiveId())

for i in range(len(cookie_list)):
    for a in range(len(active_id)):
        projectList = []
        url = f'https://zhiyou.smzdm.com/user/lottery/jsonp_draw?active_id={active_id[a]}'
        rewardurl= f'https://zhiyou.smzdm.com/user/lottery/jsonp_get_active_info?active_id={active_id[a]}'
        infourl = 'https://zhiyou.smzdm.com/user/'
        headers = {
            'Host': 'zhiyou.smzdm.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': cookie_list[i],
            'User-Agent': 'smzdm_android_V10.4.40 rv:880 (Mi-4c;Android5.1.1;zh)smzdmapp',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'https://m.smzdm.com/',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        try:
            response = requests.post(url=url, headers=headers).text
            response_info = requests.get(url=infourl, headers=headers).text
            response_reward = requests.get(url=rewardurl, headers=headers)
            result_reward = json.loads(response_reward.text)
            name = str(re.findall('<a href="https://zhiyou.smzdm.com/user"> (.*?) </a>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
            level = str(re.findall('<img src="https://res.smzdm.com/h5/h5_user/dist/assets/level/(.*?).png\?v=1">', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
            gold = str(re.findall('<div class="assets-part assets-gold">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
            silver = str(re.findall('<div class="assets-part assets-prestige">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
            data = json.loads(response)
            print('帐号' + str(i + 1)+ ' VIP'+ level + ' ' + name + ' ' + data['error_msg']+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
            time.sleep(2)
        except:
            pass    
