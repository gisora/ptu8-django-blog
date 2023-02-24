from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic
# from django.http import HttpResponse
from . import models

# Create your views here.
def index(request):
    # posts = models.Post.objects.all()
    posts = models.Post.objects.filter(status='p')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context=context)

class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_queryset(self):
        qs =  super().get_queryset().filter(status='p')
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__last_name__startswith=query)
            )
        return qs


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = 'blog/post_detail.html'


class AuthorListView(generic.ListView):
    model = models.User
    template_name = 'blog/author_list.html'
    paginate_by = 4

    def get_queryset(self):
        qs =  super().get_queryset().annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__startswith=query) 
            )
        return qs


class AuthorDetailView(generic.DetailView):
    model = models.User
    template_name = 'blog/author_detail.html'