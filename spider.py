import requests
import re
import bs4
import pdb
import time
import random

today = time.localtime()
if today[1] < 11:
    mon = "0" + str(time.localtime()[1])
today = str(today[0]) + "." + mon + "." + str(today[2])
if today[-2] == '.':
    today = today[:8] + '0' + today[-1]

def get_html():
    url = "http://www.pkulaw.cn/cluster_form.aspx?Db=news&menu_item=\
law&EncodingName=&keyword=&range=name&"

    kv={"Referer":"http://www.pkulaw.cn/", "user-agent":'Mozilla/5.0'}
    r=requests.get(url,headers=kv)
    html = r.text
    return html

def cook_soup(h):

    soup = bs4.BeautifulSoup(h,"html.parser")
    rough = soup.find("table", {"style":"border-color:Black;border-width:\
0px;width:100%;border-collapse:collapse;"})
    count = 0
    lst = []

    for tr in rough.children:
        if isinstance(tr, bs4.element.Tag):
            #pdb.set_trace()
            try:
                content = tr.text.strip("\n") + "  " + "http://www.pkulaw.cn/" \
                + tr.a.get("href")
                content = re.findall("(\d.*)&keyword", content)[0]
                
                if tr.text.strip("\n")[-10:] == today:
                    lst.append(content)
            except:
                pass
        #count += 1
    co = 1
    new_lst = []
    #pdb.set_trace()
    if len(lst) > 9:
        for i in lst[-5:]:
            i = lst[random.randint(0,len(lst)-1)]
            lst.pop(lst.index(i))
            if i[1] == '、':
                stri = str(co) + i[1:]
            else:
                stri = str(co) + i[2:]
            co += 1
            new_lst.append(stri)
        return new_lst
    else:
        lst = lst[0:5]
        return lst

    
def main():
    h1 = get_html()
    lst = cook_soup(h1)
    if lst == []:
        print("今日暂时没有新闻或重新运行试试？")
        for i in lst:
            print(i)
    else:
        print("今日法律新闻:")
        for i in lst:
            print(i)

main()
