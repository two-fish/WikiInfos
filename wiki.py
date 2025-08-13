import  requests
import  re
import time
import sys

sta=time.time()

def spaceList(cookies):         #获取所有目录ID
    num = 0
    head = {"cookie": cookies}
    while True:
        url = domain+"/rest/api/space?limit=24&start=%s" % num
        a = requests.get(url, headers=head).json()
        for i in a["results"]:
            keys.update({i["key"]})
        size = a["size"]
        if size < 24:
            break
        else:
            num += 24

def contentId(key,cookies):  #获取目录下所有文件
    ids = list()
    num = 0
    head = {"cookie": cookies.strip()}
    while True:
        url = domain+"/rest/api/space/{}/content?limit=24&start={}".format(key,num)
        a = requests.get(url, headers=head).json()
        try:
            page=a["page"]["results"]
        except:
            print("请检查Cookie或者key值。")
            break
        for i in page:
            ids.append(i["id"])
        size = a["page"]["size"]
        if size < 24:
            break
        else:
            num += 24
    return ids

def commentInfo(id,cookies):
    num = 0
    comment=[]
    head = {"cookie": cookies.strip()}
    while True:
        url = "{}/rest/api/content/{}/child/comment?expand=body.view&depth=all&limit=24&start={}".format(domain,id,num)
        a = requests.get(url, headers=head).json()
        if a["size"]:
            for i in a["results"]:
                comment.append(i["body"]["view"]["value"])
        if a["size"] < 24:
            break
        else:
            num+=24

def contentInfo(id,cookies):
    num = 0
    head = {"cookie": cookies.strip()}
    url = "{}/rest/api/content/{}?expand=body.storage&depth=all&limit=24&start={}".format(domain,id,num)
    a = requests.get(url, headers=head).json()
    txt=a["body"]["storage"]["value"]
    return txt

def fileProcessing(strs,id):      #文件处理，匹配正则筛选结果

    strs=strs.replace("[root@","")   #通过替换关键字的方法来做精度过滤，从而过滤一些误报率较高的关键字

    
    reg=re.compile(ruleString,re.I|re.M|re.S)
    qq=re.findall(reg,strs)
    if qq:
        asdf.write("\n此项目可能存在敏感数据泄露，其完整路径为：{}/pages/viewpage.action?pageId={}".format(domain,id)+ "\n")
        for i in qq:
            try:
                asdf.write(str(i)+"\n")
            except:
                print("请检查Cookie或者key值。")
                print(path)


def main(cookies):

    spaceList(cookies)
    for i in keys:
        ids=contentId(i,cookies)
        if ids:
            for w in ids:
                com = commentInfo(w,cookies)
                txt = contentInfo(w,cookies)
                if txt:
                    fileProcessing(txt,w)
                if com:
                    for e in com:
                        fileProcessing(e,w)


if __name__=="__main__":
    domain=sys.argv[1].rstrip("/")
    cookies=sys.argv[2]     #ccokie自行抓包填完整内容，如JSESSIONID=3ECBXXXXX86C263XXX3254EBDA9B2C43，请注意不能有空格
    
    keys = set()
    ruleString = ""
    with open("keyWord.txt", "r") as qwer:
        for i in qwer.readlines():
            ruleString += ".{0,80}" + i.strip() + ".{0,80}|"
        qwer.close()
    ruleString = ruleString.rstrip("|")


    asdf = open("666.html", "a+", encoding='utf-8')
    main(cookies)
    asdf.close()

    end = time.time()
    print(end - sta)

    #使用方法为 python wiki.py http://xxx.xxx.com  JSESSIONID=XXXX

