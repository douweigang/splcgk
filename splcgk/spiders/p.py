# -*- coding: utf-8 -*-
import re

import scrapy
import json
import random
from aoyun.util import user_agent

from splcgk.items import SplcgkItem


class ProclamationSpider(scrapy.Spider):
    name = 'p'
    page = 500
    start_urls = ['https://splcgk.court.gov.cn/gzfwww//ktgglist?pageNo={}']

    headers = {
        "User-Agent": random.choice(user_agent.USER_AGENTS),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://splcgk.court.gov.cn/gzfwww//ktgg",
        "Host": "splcgk.court.gov.cn",
        "Origin": "https://splcgk.court.gov.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    def start_requests(self):
        for i in range(1, self.page + 1):
            data = {
                "pageNum": "{}".format(i)
            }
            yield scrapy.FormRequest(self.start_urls[0].format(i), headers=self.headers, formdata=data)

    def parse(self, response):
        html = json.loads(response.body.decode())

        datas = html.get("data")
        for data in datas:

            item = SplcgkItem()
            item["ssxq"] = data.get("ssxq")
            item["cbgMc"] = data.get("cbgMc")
            if item["cbgMc"]:
                item["cbgMc"] = item["cbgMc"].split(":")[1] if ":" in item["cbgMc"] else item["cbgMc"]
                if len(item["cbgMc"]) == 0:
                    item["cbgMc"] = None
            item["cygMc"] = data.get("cygMc")
            if item["cygMc"]:
                item["cygMc"] = item["cygMc"].split(":")[1] if ":" in item["cygMc"] else item["cygMc"]
            item["cslfyMc"] = data.get("cslfyMc")
            item["sf"] = data.get("sf")
            item["tnr"] = data.get("tnr")

            if item["tnr"]:
                item["date"] = re.findall(r"院定于(.*?)在",item["tnr"], re.S)[0] if re.findall(r"院定于(.*?)在",item["tnr"],re.S) else None
            item["ccbftBh"] = data.get("ccbftBh")
            item["cajlb"] = data.get("cajlb")
            item["dtFbsj"] = data.get("dtFbsj")
            item["cah"] = data.get("cah")
            yield item

