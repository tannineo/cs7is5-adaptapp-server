from flask import current_app, g

from model.picture import Picture

def get_by_tag(search_string):
    pictures = Picture.objects(tags=search_string)
    return pictures

def upload(name, img_url, tags):
    picture = Picture()
    picture.name = name
    picture.img_url = img_url
    
    picture.tags = tags
    picture.save()
    return picture