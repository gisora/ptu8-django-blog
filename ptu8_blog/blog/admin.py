from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated', 'display_comments_count')
    inlines = (CommentInline, )
    list_filter = ('category', 'created')

    fieldsets = (
        ('Heading', {'fields': ('title', ('author', 'status'))}),
        ('Content', {'fields': ('text', 'category')}),
    )    


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'posted')


# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)