import os
import json
from random import randint
from simpledu.models import User, Course, Chapter
from simpledu.exts import  db
from faker import Faker
from  simpledu.app import create_app
app=create_app("development")
app.app_context().push()
fake = Faker()


# 生成一个教师用户
def item_teacher():
    user=User(username='Jack Lee',email='1223765504@qq.com',password='123456x',job='Python工程师')
    return user


def item_course():
    author = User.query.filter_by(username="Jack Lee").first()
    with open("course.json", 'r', encoding="utf8") as f:
        course = json.load(f)
        for c in course:
            yield Course(
                name=c['title'],
                description=c['content'],
                image_url=c['image_url'],
                author=author

            )


def item_chapters():
    for course in Course.query:
        # 每个课程生成3-9个章节
        for i in range(randint(3, 10)):
            yield Chapter(
                name=fake.sentence(),
                course=course,
                video_url="https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4",
                video_duration='{}:{}'.format(randint(10, 30), randint(10, 59))
            )


def run():

    db.session.add(item_teacher())
    for course in item_course():
        db.session.add(course)
    for chpater in item_chapters():
        db.session.add(chpater)
    try:
        db.session.commit()
        print("数据生成完成")
    except Exception as e:
        print(e.args)
        db.session.rollback()


if __name__ == '__main__':
    run()
