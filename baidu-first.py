# -*- coding: utf-8 -*-
import requests
from lxml import etree

def search_by_word(word):
    '''
    百度搜索
    :param word:搜索关键字
    :return: 搜索结果第一页，包含主题和链接的字典
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        "cookie": "BAIDU_SSP_lcr=https://www.infoq.cn/article/xpLOXrpaeaNDtW5zbE8m; BAIDUID=0E6A1FE4072F5695B1466CE7BC13A4F6:FG=1; BIDUPSID=0E6A1FE4072F5695B1466CE7BC13A4F6; PSTM=1555344421; H_WISE_SIDS=131798_124612_127759_100807_131835_131824_128068_131676_131889_132019_120141_132311_132440_130763_132394_132379_132325_132212_131518_132261_118897_118873_131402_118842_118823_118792_132245_131649_131576_131536_131534_131530_130222_131294_131871_131390_129564_107318_131795_131396_130127_132239_131873_130570_131196_130350_132387_129656_131247_127026_131435_131687_132538_131035_131905_132294_132090_131046_130058_129901_128891_129644_132204_130828_131172_131447_110085_131769_127969_131506_123290_130819_131749_132282_127416_131708_131827_131750_131265_131262_128604_131258_131959_100460; BD_UPN=123253; BDSFRCVID=jsCOJeCmH6l9L5vwwHBH-fIpz2KK0gOTHbibSj6UMFCr5-IVJeC6EG0Ptf8g0KubvZQgogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8oK-atDvbfP0kMboH5PLt-Uvy-40XKKOLVb6j2-OkeqOJ2Mt5MxDI0lJ0LU3EyTnJhDt53bDMb-b9L63vM5tpeGLfq6tJJRusL-35HJnhHt3NMtbShnLOqxby26n-24jeaJ5n0-nnhnctXq5bMq0qXM6UtU0JbevK_In2Mp_2OnPRy6Cae5Q-Da_Dq6n2aIOt0Tr25RrjeJrmq4bohjnBynn9BtQmJJuq5DbdQUbbo4jtDCctyJ8rhPjgBUo2Qg-q3R7PKRkV8JOE5loAQP-Zjb5h0x-jLgbhVn0MW-5DDI3cD-nJyUP-D4nnBTcR3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRu_CF-tD8WMK_GjTRb5nbHMUrfaRJ-K-o2WbCQLRnr8pcNLTDKLU330UDf-hTdbHuL0qTMLn5vhx530qO1j4_e3aQqBbQ7QCQM_xIXKljNDl5jDh3rb6ksD-Rt5JcGfCny0hvcMCocShPwQMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDHt8JT-tJJ32Wn7a5TrMeJrnbtTMq4tehHnhbtRL-KOtQJOHqR3bJRO6q6KKDjjLDGtXJjDDtJCH_5u-tDDKhD_6JRoMhq4DbfO0-4u_K5Rb8t52ax7EeK6T5n6j5I6XDGLHJ6DfHJuHoC_htD0_hC_lD6LKjTnBQ4ReBtQm05bxobcPaqcbbJbG-UnpynIXLN0OtP7EKD-OKRLbWDFKMDI4DjL2DjPEhMrMan3eHD7JQJTMHJOoDDvFKUbcy4LdhtAq2TcrJ6cfLhnPWT6tOtJuDxRvD--g3-7aa4jg2JcP2lQn-DKVOfQ_bf--QfbQ0hOhqP-jW5TaLfcl5b7JOpkxbUnxy5KUQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6T2-DA_VCL5JUK; MCITY=-284%3A; H_PS_PSSID=1457_21091_18559_29568_29221; BDUSS=NiSkVJaHNNdXhFMzNIU250bENmblZwOWR2UVpzcDZmaU5kampjOFNJTH5pZUJkRUFBQUFBJCQAAAAAAAAAAAEAAADvWOgFa2M0MTk2OTQ4NTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP~8uF3~~LhdUz; sugstore=0; H_PS_645EC=6e97QXluum%2FlnSENyh75vubOxVkQgyvS2ZhSv9npHXp4xRP40XVV3X5Yz9cpqWc04zUx; BDSVRTM=156; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598"
        }

    base_url = "http://www.baidu.com/"

    # 搜索百度链接
    search_url = "https://www.baidu.com/s?wd={}".format(word)

    # 执行搜索
    r = requests.get(search_url, headers=headers)
    selector = etree.HTML(r.text)

    # 获取左侧搜索结果
    course_item_list = selector.xpath("//div[contains(@class,'c-container')]")

    course_dict = {}
    for course_item in course_item_list:
        # 搜索链接
        course_url = course_item.xpath("h3/a/@href")[0]
        # 有链接是相对路径，拼接成绝对路径
        if not course_url.startswith(base_url):
            course_url = base_url + course_url

        # 搜索的主题 由于搜索关键字是em元素包裹 因此 text()包含2个斜杠 获取所有子元素文本
        course_title_list = course_item.xpath("h3/a//text()")
        course_title = ''.join(course_title_list) # 拼接成主题

        print(course_url,course_title)

        # 存放到字典
        course_dict[course_url] = course_title.strip()

    return course_dict

course_dict = search_by_word("李志文")
print(course_dict)
