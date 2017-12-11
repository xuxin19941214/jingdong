import requests
from lxml import etree
import re
from selenium import webdriver
from pymongo import MongoClient
# urls = ['https://list.jd.com/list.html?cat=1320,5019,12215',
# 'https://list.jd.com/list.html?cat=1320,5019,5020',
# 'https://list.jd.com/list.html?cat=1320,5019,5021',
# 'https://list.jd.com/list.html?cat=1320,5019,5022',
# 'https://list.jd.com/list.html?cat=1320,5019,5023',
# 'https://list.jd.com/list.html?cat=1320,5019,5024',
# 'https://coll.jd.com/list.html?sub=16366',
# 'https://list.jd.com/list.html?cat=1320,1583,1590',
# 'https://list.jd.com/list.html?cat=1320,1583,1591',
# 'https://list.jd.com/list.html?cat=1320,1583,1592',
# 'https://list.jd.com/list.html?cat=1320,1583,13757',
# 'https://list.jd.com/list.html?cat=1320,1583,1593',
# 'https://list.jd.com/list.html?cat=1320,1583,1594',
# 'https://list.jd.com/list.html?cat=1320,1583,1595']
urls = [
    # ('https://list.jd.com/list.html?cat=1320,5019,5020', 212),
    #  ('https://list.jd.com/list.html?cat=1320,5019,5021', 212),
    #   ('https://list.jd.com/list.html?cat=1320,5019,5022', 240),
    #    ('https://list.jd.com/list.html?cat=1320,5019,5023', 247),
    #     ('https://list.jd.com/list.html?cat=1320,5019,5024', 204),
         ('https://coll.jd.com/list.html?sub=16366', 74),
         #  ('https://list.jd.com/list.html?cat=1320,1583,1590', 310),
         #   ('https://list.jd.com/list.html?cat=1320,1583,1591', 223),
         #    ('https://list.jd.com/list.html?cat=1320,1583,1592', 234),
         #     ('https://list.jd.com/list.html?cat=1320,1583,13757', 113),
         #      ('https://list.jd.com/list.html?cat=1320,1583,1593', 214),
         #       ('https://list.jd.com/list.html?cat=1320,1583,1594', 243),
         #        ('https://list.jd.com/list.html?cat=1320,1583,1595', 265)
        ]

client = MongoClient('127.0.0.1', 27017)
db = client.db_jd

driver = webdriver.Chrome()
def travel_url(url, j):
    for i in range(1, j+1):
        all_repeat = True
        # list_url = url + '&page=' + str(i) + '&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
        list_url = url + '&page='+str(i)+'&JL=6_0_0'
        res = db.page_urls.find_one({'list_url': list_url})
        # 判断该页面是否被加载了
        print(list_url)
        if not res:
            try:
                driver.get(list_url)
            except:
                driver = webdriver.Chrome()
                driver.get(list_url)
            items = driver.find_elements_by_xpath(" //li[@class='gl-item']")
            # 每一个列表内容， 深入一次
            for item in items:
                # 获取详情页的url
                href = item.find_element_by_class_name('p-name').find_element_by_tag_name('a')
                # 获取详情页的 价格

                price = item.find_elements_by_tag_name('strong')
                # 终止for循环的标志， 当取到price时候，run置为False， 终止for循环，break
                run = True

                # 将价格传入详情页面
                real_href = href.get_property('href')
                if not db.page_urls.find_one({'url': real_href}):
                    for strong in price:
                        i = strong.find_elements_by_tag_name('i')
                        if not run:
                            break
                        for pri in i:
                            if not run:
                                break
                            if len(pri.text) > 3:
                                real_price = pri.text
                                run = False
                    db.page_urls.insert_one({'list_url': list_url, 'detail_url': real_href, 'price': real_price})
                    print('success:' + list_url + real_href)
                    all_repeat = False
                else:
                    pass
            # if all_repeat:
            #     print(real_href)
            #     break


for url, i in urls:
    travel_url(url, i)
