import requests,execjs
def jiemi(text):
    with open("youdao.js",'r',encoding='utf-8') as f :
        youdao_js = f.read()
    sign = execjs.compile(youdao_js).call('jiemi',text)
    data = {
        "q":text,
        "le":'en',
        "sign":sign,
        "keyfrom":"webdict"
    }
    response = requests.post("https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4",data=data)
    return response.json()['web_trans']['web-translation'][0]['trans'][0]['value']
if __name__ == '__main__':
    text = jiemi("牛马")
    print(text)

