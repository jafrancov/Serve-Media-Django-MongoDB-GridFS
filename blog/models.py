from mongoengine import *
from mongodbforms import DocumentForm


class Post(Document):
    title = StringField(max_length=160, required=True)
    body = StringField(required=True)
    image = ImageField(size=(800, 600, True))


class PostForm(DocumentForm):
    class Meta:
        document = Post
