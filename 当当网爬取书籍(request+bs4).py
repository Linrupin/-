import bs4
import requests
import xlwt


# 创建一个新的Excel工作簿和工作表
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
sheet.write(0,0,'书名')
sheet.write(0,1,'链接')
sheet.write(0,2,'作者')
sheet.write(0,3,'价格')

def create_response(page):
    url = f'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-{page}'
    headers = {
        'User-Agent':
            'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 114.0.0.0Safari / 537.36'
    }
    response =requests.get(url=url,headers = headers)
    return response

def get_content(response):
    content = response.text
    return content

def download(content,row_num):
    soup = bs4.BeautifulSoup(content,'lxml')
    list = soup.find(class_ = 'bang_list clearfix bang_list_mode').find_all('li')
    for item in list:#将数据爬取下来（书名，链接，作者，价格）
        bookname = item.find(class_ = 'name').a['title']
        src = item.find(class_ = 'name').a['href']
        author = item.find_next(class_ = 'publisher_info').text if item.find(class_= 'publisher_info') else ' '
        pay = item.find(class_ = 'price_n').text
        print(bookname,src,author,pay)

        # 将数据写入Excel表格的相应单元格
        sheet.write(row_num, 0, bookname)
        sheet.write(row_num, 1, src)
        sheet.write(row_num, 2, author)
        sheet.write(row_num, 3, pay)
        row_num+=1 # 增加行号以准备写入下一行数据
    return row_num


if __name__ == '__main__':
    start_page = int(input("请输入起始页数"))
    end_page = int(input("请输入结束页数"))
    row_num = 1
    for page in range(start_page,end_page+1):
        response = create_response(page)
        content = get_content(response)
        row_num = download(content,row_num)
    book.save(u'当当网前100本最受欢迎的书.xlsx')  # 保存Excel文件
