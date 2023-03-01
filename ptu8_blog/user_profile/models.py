from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('profile'), related_name='profile')
    avatar = models.ImageField(_('avatar'), upload_to='blog/avatars/', default='blog/avatars/default_avatar.png', null=True, blank=True)
    about = models.TextField(_('about'), max_length=500, help_text=_('about text'))

    def __str__(self):
        return self.user.username