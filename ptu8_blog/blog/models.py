from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Category(models.Model):
    name = models.CharField(_('name'), max_length=50)

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('profile'))
    avatar = models.ImageField(_('avatar'), upload_to='blog/avatars/', null=True, blank=True)


class Post(models.Model):
    title = models.CharField(_('title'), max_length=255, db_index=True, help_text=_('post title'))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author')
    )
    text = tinymce_models.HTMLField(_('text'), null=True, blank=True, help_text=_('post text'))
    category = models.ManyToManyField(
        Category,
        help_text=_('select categories for this post'),
        verbose_name=_('categories')
    )
    created = models.DateTimeField(_('created'), auto_now_add=True, help_text=_('post created'))
    updated = models.DateTimeField(_('updated'), auto_now=True, help_text=_('post updated'))

    POST_STATUS = (
        ('d', _('draft')),
        ('p', _('published'))
    )

    status = models.CharField(
        _('status'),
        max_length=1,
        choices=POST_STATUS,
        default='d',
        help_text=_('Change post status')
    )

    def display_comments_count(self):
        return self.comments.all().count()
    display_comments_count.short_description = _('comments count')

    class Meta:
        ordering = ['created']
    
    def __str__(self) -> str:
        return f"{self.author} - {self.title} ({self.updated})"
    

class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('author')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    text = models.TextField(_('text'), max_length=1000, help_text=_('comments text'))
    posted = models.DateTimeField(_('posted'), auto_now_add=True, help_text=_('comment posted'))

    class Meta:
        ordering = ['posted']

    def __str__(self) -> str:
        return f"{self.author} - {self.post} ({self.posted})"