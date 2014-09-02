from django.shortcuts import render_to_response
from blog.models import *


def blog_index(request):
    posts = Post.objects.all()
    return render_to_response('index.html', {'posts': posts})
