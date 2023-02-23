from django.shortcuts import render
from django.views import generic
# from django.http import HttpResponse
from . import models

# Create your views here.
def index(request):
    posts = models.Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context=context)

class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/post_list.html'
    paginate_by = 2


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = 'blog/post_detail.html'


class AuthorListView(generic.ListView):
    model = models.User
    template_name = 'blog/author_list.html'
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = models.User
    template_name = 'blog/author_detail.html'