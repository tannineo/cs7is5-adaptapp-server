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


def randomly_get_pics(prefered_tags=[], num=20):
    pictures = []

    if len(prefered_tags) == 0:
        pictures = Picture.objects().aggregate(*[
            {
                '$sample': {
                    'size': num
                }
            },
        ])
    else:
        count_sum = 20
        for i in range(0, len(prefered_tags)):
            if i != len(prefered_tags) - 1:
                cnt = random.randint(0, count_sum)
            else:
                cnt = count_sum
            if cnt > 0:
                pictures.extend(Picture.objects().aggregate(*[
                    {
                        '$match': {
                            'tags': {
                                '$eq': prefered_tags[i]
                            }
                        }
                    },
                    {
                        '$sample': {
                            'size': cnt
                        }
                    },
                ]))
                count_sum -= cnt

    random.shuffle(pictures)
    return pictures


def upload(name, img_url, tags):
    picture = Picture()
    picture.name = name
    picture.img_url = img_url
    picture.tags = tags
    picture.save()
    return picture


def change_likes_of_pic(pic_id, num=1):
    pic_list = Picture.objects(id=pic_id)
    if (len(pic_list) <= 0):
        current_app.logger.info('change_likes_of_pic find id=' + str(pic_id) +
                                ' cannot find the pic')
        return

    pic = pic_list[0]
    current_app.logger.info('change_likes_of_pic find id=' + str(pic_id) +
                            ' to change it num by ' + str(num) +
                            ' the original is :' + str(pic.likes))
    pic.likes = pic.likes + num
    pic.save()


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
