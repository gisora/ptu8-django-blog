from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from . import models, forms

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


class PostDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Post
    template_name = 'blog/post_detail.html'
    form_class = forms.PostCommentForm

    def get_success_url(self) -> str:
        return reverse('post-detail', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['post'] = self.get_object()
        initial['commenter'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.commenter = self.request.user
        form.save()
        messages.success(self.request, 'Commment posted successfully')
        return super().form_valid(form)



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

class AuthorPostsListView(LoginRequiredMixin, generic.ListView):
    model = models.Post
    template_name = 'blog/author_posts_list.html'
    context_object_name = 'author_posts_list'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs
    

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    template_name = 'blog/post_create_update.html'
    fields = ('title', 'text', 'category', 'status')
    success_url = reverse_lazy('author-posts-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'd'
        if self.request.GET.get('post_id'):
            initial['post'] = get_object_or_404(models.Post, id=self.request.GET.get('post_id'))
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'd'
        messages.success(self.request, f'Post "{form.instance.title}" successfully created.')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = models.Post
    template_name = 'blog/post_create_update.html'
    fields = ('title', 'text', 'category', 'status')
    success_url = reverse_lazy('author-posts-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post "{form.instance.title}" successfully updated.')
        return super().form_valid(form)
    
    def test_func(self):
        return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = models.Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('author-posts-list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, f'Post seccessfully deleted.')
        return super().form_valid(form)