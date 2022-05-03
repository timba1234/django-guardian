from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm


class Post(models.Model):
    title = models.CharField('title', max_length=64)
    slug = models.SlugField(max_length=64)
    content = models.TextField('content')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    tenant = models.TextField('tenant', default='shared')
    exclude = ('tenant')

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_post', 'Can view post'),
        )
        get_latest_by = 'created_at'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts_post_detail', args=(), kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        group = Group.objects.get(name=self.tenant)
        super(Post, self).save(*args, **kwargs)
        assign_perm('view_post', group, self)

