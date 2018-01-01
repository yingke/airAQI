# coding: utf-8

#获取2017年全年全国AQI日报指数
#

import requests
import time
from bs4 import BeautifulSoup
import pymongo
import json
import datetime

# 请求头信息


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '10749',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'datacenter.mep.gov.cn:8099',
    'Origin': 'http://datacenter.mep.gov.cn:8099',
    'Referer': 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action',
     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

url ='http://datacenter.mep.gov.cn:8099/ths-report/report!list.action';


def main():

    connection = pymongo.MongoClient('localhost', 27017);
    ##连接airdata数据库，没有则自动创建
    tdb = connection.airdata;
    #连接airdatas 集合 没有则自动创建

    post = tdb.airdatas;

    for i in range(1,4445):
      params = {'page.pageNo': i, 'xmlname': 1462259560614, 'queryflag': 'close', 'V_DATE': '2017-01-01',
                  'E_DATE': '2017-12-31'};
      html = requests.post(url, data=params,headers=headers);
      soup = BeautifulSoup(html.text, 'html.parser');
      array = json.loads(soup.find(id="gisDataJson")["value"])
      date = datetime.datetime.now().strftime('%H:%M:%S')
      print(u"第%s次运行 时间：%s (获取：%s数据)" % (i, date, len(array)))
      post.insert(array);
      time.sleep(3)


if __name__=='__main__':
    main()

