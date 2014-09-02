from mongoengine import *
from mongodbforms import DocumentForm


class Post(Document):
    title = StringField(max_length=160, required=True)
    body = StringField(required=True)
    pic = ImageField(size=(800, 600, True))


class PostForms(DocumentForm):
    class Meta:
        document = Post
