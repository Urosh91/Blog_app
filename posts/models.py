from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from django.utils.text import slugify
from markdown_deux import markdown
from comments.models import Comment

from .utils import read_time


class PostManager(models.Manager):
    def all_published(self, *args, **kwargs):
        return super(PostManager, self).filter(share_public=True)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True,
                              height_field='image_height', width_field='image_width')
    image_width = models.IntegerField(default=0)
    image_height = models.IntegerField(default=0)
    share_public = models.BooleanField(default=True)
    content = models.TextField()
    read_time = models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    class Meta:
        ordering = ['-created_at', '-updated']

    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    def get_content_type(self):
        contentt_type = ContentType.objects.get_for_model(self.__class__)
        return contentt_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    post = Post.objects.filter(slug=slug).order_by('-id')
    exists = post.exists()
    if exists:
        new_slug = f'{slug}-{post.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_data = instance.get_markdown()
        get_read_time = read_time(html_data)
        instance.read_time = get_read_time


pre_save.connect(pre_save_post_receiver, sender=Post)