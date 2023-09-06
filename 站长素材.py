
import urllib.request
from lxml import etree

def create_request(page):
    if(page ==1):
        url = "https://sc.chinaz.com/tupian/index.html"
    else:
        url = f"https://sc.chinaz.com/tupian/index_{page}.html"
    headers = {
         "User-Agent":
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
     }
    requests = urllib.request.Request(url = url,headers= headers)
    return requests

def get_content(requests):
    response = urllib.request.urlopen(requests)
    content = response.read().decode('utf-8')#得到网页的源码
    return content

def down_load(content):
    #下载图片是 ： urllib.request.urlretrieve("图片/视频地址","文件/视频名字")
    tree = etree.HTML(content)
    name_list = tree.xpath('//div[@class="tupian-list com-img-txt-list"]//img/@alt')#从源码content中获得标题信息(网站上的图片名)
    src_list = tree.xpath('//div[@class="tupian-list com-img-txt-list"]//img/@data-original')#网站上的图片链接，后续需要用到urlretrieve时有用
    for i in range(len(name_list)):
        name = name_list[i]
        src = src_list[i]#前缀少了https:后面给他加上
        url = "https:"+src#真实的地址
        urllib.request.urlretrieve(url = url,filename='./img111111/' + name + '.jpg')#url是链接，filename是图片下载地址及名称


if __name__ == '__main__':
    start_page = int(input("请输入起始页码："))
    end_page = int(input("请输入结束页码："))

    for page in range(start_page,end_page+1):
        requests = create_request(page) #1请求对象定制
        content = get_content(requests) #获取网页源码
        down_load(content)#下载


