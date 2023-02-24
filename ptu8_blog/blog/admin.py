from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_full_name', 'created', 'updated', 'display_comments_count')
    inlines = (CommentInline, )
    list_filter = ('category', 'created')

    fieldsets = (
        ('Heading', {'fields': ('title', ('author', 'status'))}),
        ('Content', {'fields': ('text', 'category')}),
    )    
    
    search_fields = ('title', 'author')

    def display_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
    display_full_name.short_description = _('author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'display_email', 'post', 'posted')
    list_filter = ('posted',)
    search_fields = ('author', 'display_email', 'post')

    def display_email(self, obj):
        return obj.author.email
    display_email.short_description = _('email')

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserProfile)