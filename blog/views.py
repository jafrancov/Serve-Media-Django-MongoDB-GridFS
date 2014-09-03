from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from mongoengine.django.shortcuts import get_document_or_404
from bson.objectid import ObjectId
from pymongo import Connection
import gridfs
from blog.models import *


def blog_index(request):
    posts = Post.objects.all()
    return render_to_response('index.html', {'posts': posts})


# View Post without thumbnail
def view_post(request, id):
    post = get_document_or_404(Post, pk=id)
    # Create temporal key img_id in order to get the image by ID
    # If there is no image, doesn't show it in the post
    try:
        post.img_id = post.image._id
    except AttributeError:
        post.img_id = False
    return render_to_response('post.html', {'post': post})


# View Post with thumbnail
def view_post_th(request, id):
    post = get_document_or_404(Post, pk=id)
    # Create temporal key img_id in order to get the image by ID
    # If there is no image, doesn't show it in the post
    try:
        post.img_id = post.image._id
    except AttributeError:
        post.img_id = False
    try:
        post.thumbnail_id = post.image.thumbnail_id
    except AttributeError:
        post.thumbnail_id = False
    return render_to_response('post2.html', {'post': post})


def add_post(request):
    if request.method == 'POST':
        # MUST specify the request.FILES
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return render_to_response('add.html', {'form': form},
                                      context_instance=RequestContext(request))
        form.save()
        return HttpResponseRedirect(reverse('blog.views.blog_index'))
    else:
        form = PostForm()
        return render_to_response('add.html', {'form': form},
                                  context_instance=RequestContext(request))


# Method 1, regular image
def display_image(request, id):
    image = get_document_or_404(Post, image=ObjectId(id)).image
    return HttpResponse(image.read(), content_type=image.contentType)


# Method 2, if image could be a thumbnail, with the ORM there is no direct
# way to access the thumbnail image, that's the reason of this method.
def display_image_m2(request, id):
    # Additional connection to access the File System of MongoDB
    mongo_con = Connection()
    # If the field is ImageField, the collection is 'images'
    grid_fs = gridfs.GridFS(mongo_con.servemedia, collection='images')
    if not grid_fs.exists(ObjectId(id)):
        raise Exception("Mongo file does not exist! {0}".format(ObjectId(id)))
    image = grid_fs.get(ObjectId(id))
    try:
        content_type = image.contentType
    except AttributeError:
        for grid_out in grid_fs.find({'thumbnail_id': ObjectId(id)}).limit(1):
            content_type = grid_out.contentType
    return HttpResponse(image.read(), content_type=content_type)
