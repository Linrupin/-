import requests
from bs4 import BeautifulSoup
import xlwt
# 创建一个新的Excel工作簿和工作表
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'评分')
sheet.write(0,2,'导演')
sheet.write(0,3,'简介')
sheet.write(0,4,'链接')

def create_response(page):
    url = f'https://movie.douban.com/top250?start={page}&filter='# 构建URL来获取豆瓣Top250电影的页面
    headers = {
        'User-Agent':
           'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 114.0.0.0Safari / 537.36'
    }
    response = requests.get(url=url, headers=headers) # 发送HTTP GET请求获取页面内容
    return response

def get_content(response):
    text = response.text # 提取HTTP响应的文本内容
    return text

def download(text,row_num):
    soup = BeautifulSoup(text,'lxml') # 使用BeautifulSoup解析HTML文本
    list = soup.find(class_= 'grid_view').find_all('li') # 查找电影列表
    for item in list:
        item_name = item.find(class_ = 'title').string # 获取电影名称
        item_score = item.find(class_='rating_num').string  # 获取电影评分
        item_director = item.find('p').text.strip().split('\n')[0] # 获取导演信息
        item_intr = item.find(class_='inq').string if item.find(class_='inq') else '' # 获取电影简介，如果不存在简介则为空字符串
        item = item.find('a').get('href')#取得链接

        # 将数据写入Excel表格的相应单元格
        sheet.write(row_num, 0, item_name)
        sheet.write(row_num, 1, item_score)
        sheet.write(row_num, 2, item_director)
        sheet.write(row_num, 3,  item_intr)
        sheet.write(row_num, 4, item)
        row_num+=1 # 增加行号以准备写入下一行数据
    return row_num




if __name__ =='__main__':
    start_page = int(input("请输入起始页码："))
    end_page = int(input("请输入结尾页码："))
    row_num = 1 # 初始化行号
    for page in range(start_page,end_page+1,25):
        response = create_response(page)
        content  = get_content(response)
        row_num = download(content,row_num) # 将数据写入Excel表格
    book.save(u'豆瓣最受欢迎的250部电影.xlsx') # 保存Excel文件