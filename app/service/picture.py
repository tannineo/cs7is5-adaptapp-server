from flask import current_app, g
import random

from model.picture import Picture

available_tags = [
    'butterfly', 'cat', 'dog', 'ox', 'squirrel', 'elephant', 'sheep',
    'chicken', 'horse', 'spider'
]


def get_by_tag(search_string, num=20):
    pictures = Picture.objects[:20](tags=search_string)
    return pictures


def randomly_get_pics(num=20):
    # TODO: aggregate random
    pictures = Picture.objects[:num]()
    return pictures


def upload(name, img_url, tags):
    picture = Picture()
    picture.name = name
    picture.img_url = img_url
    picture.tags = tags
    picture.save()
    return picture


def once_load_all():
    for str_tag in available_tags:
        for i in range(1, 21):
            snum = str(i)
            while len(snum) < 5:
                snum = '0' + snum

            picture = Picture()
            picture.name = snum + '-' + str_tag
            picture.img_url = '/' + snum + '-' + str_tag + '.jpg'
            picture.tags = [str_tag]
            picture.likes = random.randint(0, 666)

            picture.save()
