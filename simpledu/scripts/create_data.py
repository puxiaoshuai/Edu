import os
import json
from random import randint
from simpledu.models import db,User,Course,Chapter
from  faker import Faker
fake=Faker()
#生成一个教师用户
def item_teacher():
    yield User(
        username='Jack Lee',
        email='1223765504@qq.com',
        password='123456x',
        job='Python工程师'
    )
def item_course():
    author=User.query.filter_by(username="Jack Lee").first()

    with open("course.json",'r',encoding="utf8") as f:
        course=json.load(f)
        for c in course:
            yield Course(
                name=c['title'],
                description=c['content'],
                image_url=c['image_url'],
                author=author

            )

def item_chapters():
    for course in Course.query:
        print(course)
if __name__ == '__main__':
    a=Course.query.all()
    print(a)