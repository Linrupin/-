import re, jsonpath, requests, hashlib, time, openpyxl, threading
from multiprocessing.dummy import Pool


def verify(field):
    if field:
        return field[0]
    else:
        return ''



def createParams(sign):
    params = {
        'jsv': '2.7.0',
        'appKey': value,
        't': stamp,
        'sign': sign,
        'api': 'mtop.1688.shop.data.get',
        'v': '1.0',
        'type': 'json',
        'valueType': 'string',
        'dataType': 'json',
        'timeout': '10000',
    }
    #print(params)
    return params



def createData1(memberId, page):
    data1 = r'{"dataType":"moduleData","argString":"{\"memberId\":\"%s\",\"appName\":\"pcmodules\",\"resourceName\":\"wpOfferColumn\",\"type\":\"view\",\"version\":\"1.0.0\",\"appdata\":{\"sortType\":\"wangpu_score\",\"sellerRecommendFilter\":false,\"mixFilter\":false,\"tradenumFilter\":false,\"quantityBegin\":null,\"pageNum\":%s,\"count\":30}}"}' % (memberId, str(page))
    return data1



def md5_string(in_str):
    md5 = hashlib.md5()
    md5.update(in_str.encode("utf8"))
    result = md5.hexdigest()
    return result


def createData(memberId,page):
    data = {
        'data': '{"dataType":"moduleData","argString":"{\\"memberId\\":\\"%s\\",\\"appName\\":\\"pcmodules\\",\\"resourceName\\":\\"wpOfferColumn\\",\\"type\\":\\"view\\",\\"version\\":\\"1.0.0\\",\\"appdata\\":{\\"sortType\\":\\"wangpu_score\\",\\"sellerRecommendFilter\\":false,\\"mixFilter\\":false,\\"tradenumFilter\\":false,\\"quantityBegin\\":null,\\"pageNum\\":%s,\\"count\\":30}}"}' % (memberId, page),
    }

    return data




def crawl(page):
    page_content = f'{token}&{stamp}&{value}&{createData1(memberId, page)}'
    page_sign = md5_string(page_content)
    response = requests.post('https://h5api.m.1688.com/h5/mtop.1688.shop.data.get/1.0/', params=createParams(page_sign),
                             headers=headers, data=createData(memberId, str(page))).json()

    offerList = jsonpath.jsonpath(response, '$.data.content.offerList.*')
    #print(len(offerList))

    for product in offerList:
        agentPrice = jsonpath.jsonpath(product, '$..agentPrice')[0]
        agentBookedCount = jsonpath.jsonpath(product, '$..agentBookedCount')[0]
        #bookedCount = jsonpath.jsonpath(product, '$..bookedCount')[0]
        #categoryId = jsonpath.jsonpath(product, '$..categoryId')[0]
        gmtCreate = jsonpath.jsonpath(product, '$..gmtCreate')[0]
        gmtExpire = jsonpath.jsonpath(product, '$..gmtExpire')[0]
        id = jsonpath.jsonpath(product, '$..id')[0]
        ninetySaleQuantity = jsonpath.jsonpath(product, '$..ninetySaleQuantity')[0]
        imageURI = jsonpath.jsonpath(product, '$..imageURI')[0]
        newProduct = jsonpath.jsonpath(product, '$..newProduct')[0]
        quantityBegin = jsonpath.jsonpath(product, '$..quantityBegin')[0]
        #quantitySumMonth = jsonpath.jsonpath(product, '$..quantitySumMonth')[0]
        #saleQuantity = jsonpath.jsonpath(product, '$..saleQuantity')[0]
        subject = jsonpath.jsonpath(product, '$..subject')[0]
        offerPrice = jsonpath.jsonpath(product, '$..offerPrice')[0]
        fullName = jsonpath.jsonpath(product, '$..fullName')[0]
        thirtyBookCount = verify(jsonpath.jsonpath(product, '$..thirtyBookCount'))
        thirtyGmv = verify(jsonpath.jsonpath(product, '$..thirtyGmv'))
        thirtySaleQuantity = verify(jsonpath.jsonpath(product, '$..thirtySaleQuantity'))
        link = f'https://detail.1688.com/offer/{id}.html'

        lock.acquire()
        sheet.append([id,link,newProduct,fullName,gmtCreate,gmtExpire,subject,imageURI,offerPrice,quantityBegin,agentPrice,agentBookedCount,thirtyBookCount,thirtySaleQuantity,thirtyGmv,ninetySaleQuantity])
        lock.release()

    print(f'**第{page}页爬取完成**')


if __name__ == '__main__':
    store = input('请输入店铺地址：如(shop8737105u7f4c8.1688.com) ')
    cookie = input('请输入cookie: ')


    headers1 = {
        'authority': store,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        'cookie': cookie,
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': f'https://{store}/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    }

    res = requests.get(f'https://{store}/page/offerlist.htm', headers=headers1).text
    memberId = re.findall('"memberId":"(.*?)"', res, re.S)[0]
    companyName = re.findall('"companyName":"(.*?)"', res, re.S)[0]


    headers = {
        'authority': 'h5api.m.1688.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        'cookie': cookie,
        'dnt': '1',
        'origin': 'https://shop1p6598l279491.1688.com',
        'pragma': 'no-cache',
        'referer': 'https://shop1p6598l279491.1688.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    }


    wb = openpyxl.Workbook()
    sheet = wb.active
    header = ['产品ID','产品链接','新品','类目名称','创建时间','过期时间','标题','主图','价格','起订量','代理价','代理订购量','30天订购量','30天销售数量','30天销售额','90天销售数量']
    sheet.append(header)

    lock = threading.Lock()
    token = re.findall('_m_h5_tk=(.*?)_\d+;', cookie, re.S)[0]
    stamp = round(time.time() * 1000)
    value = '12574478'

    content = f'{token}&{stamp}&{value}&{createData1(memberId, "1")}'
    Sign = md5_string(content)

    response = requests.post('https://h5api.m.1688.com/h5/mtop.1688.shop.data.get/1.0/', params=createParams(Sign),
                             headers=headers, data=createData(memberId, '1')).json()
    #print(response)
    offersCount = int(jsonpath.jsonpath(response, '$.data.content.offerSumm.offersCount')[0])

    if (offersCount % 30) != 0:
        totalPage = (offersCount // 30) + 1
    else:
        totalPage = offersCount // 30

    print(f'总页数：{totalPage}，总产品数：{offersCount}')

    pool = Pool()
    pool.map(crawl, [i for i in range(1, totalPage+1)])
    wb.save(f'1688全店-{companyName}.xlsx')
    input(f'1688全店-{companyName}.xlsx *** 爬取完成')