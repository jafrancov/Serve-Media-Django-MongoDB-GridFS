from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.core.urlresolvers import reverse
from mongoengine.django.shortcuts import get_document_or_404
from blog.models import *


def blog_index(request):
    posts = Post.objects.all()
    return render_to_response('index.html', {'posts': posts})


def view_post(request, id):
    post = get_document_or_404(Post, pk=id)
    # Create temporal key img_id in order to get the image by ID
    post.img_id = post.image._id
    return render_to_response('post.html', {'post': post})


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
