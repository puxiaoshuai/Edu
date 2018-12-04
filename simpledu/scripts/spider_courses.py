import requests
from bs4  import BeautifulSoup
import  json
url="https://www.shiyanlou.com/bootcamp/"

try:
    response=requests.get(url)
    if response.status_code==200:
        text=response.text
        bs=BeautifulSoup(text,'lxml')
        div_item=bs.find_all("div",class_='bootcamp-courses-item')
        courses=[]

        for x in div_item:
            course = {}
            a_s=x.find_all('a')
            image=x.find_all("img")[0]["src"]
            title=a_s[1].find("span").string.strip()
            content = a_s[2].find("p").string.strip()
            course['image_url']=image
            course['title']=title
            course['content']=content
            courses.append(course)
            print(a_s)
        with open("course.json",'w',newline="\n",encoding='utf8') as f:
            f.write(json.dumps(courses))


except Exception as err:
    print(err.args)