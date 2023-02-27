from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
# from django.http import HttpResponse
from . import models

# Create your views here.
def index(request):
    # posts = models.Post.objects.all()
    # posts = models.Post.objects.filter(status='p')
    paginator = Paginator(models.Post.objects.filter(status='p'), 2)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)
        
    context = {
        'posts': paged_posts,
    }
    return render(request, 'blog/index.html', context=context)

class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs =  super().get_queryset().filter(status='p')
        
        category_id = self.request.GET.get('category_id')
        if category_id:
            qs = qs.filter(category=category_id)

        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__last_name__startswith=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = models.Category.objects.all()
        context.update({'categories': categories})
        category_id = self.request.GET.get('category_id')
        if category_id:
            selected_category = get_object_or_404(models.Category, id=category_id)
            context.update({'selected_category': selected_category})
        return context


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = 'blog/post_detail.html'

class AuthorListView(generic.ListView):
    model = models.User
    template_name = 'blog/author_list.html'
    context_object_name = "authors_list"
    paginate_by = 10

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
    context_object_name = "author"