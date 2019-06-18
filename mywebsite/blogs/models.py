from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    class Meta:
        verbose_name='Post'
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE,)
    title=models.CharField(max_length=100)
    content=models.TextField()
    createtime=models.DateTimeField(default=timezone.now)
    publishtime=models.DateTimeField(blank=True,null=True)

    def publishpost(self):
        self.publishtime=timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    def approved_comments(self):
        return self.comments.filter(approve_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        verbose_name='Comment'
    post=models.ForeignKey('blogs.Post',related_name='comments',on_delete=models.CASCADE,)
    author=models.CharField(max_length=100)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now)
    approve_comment=models.BooleanField(default=False)

    def approve(self):
        self.approve_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
