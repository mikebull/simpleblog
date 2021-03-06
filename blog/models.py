# -*- coding:utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    '''
    A class to group related blog posts
    '''
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return u'/%s/%s/' % ('categories', self.slug)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title).lower()
        super(Category,self).save(*args, **kwargs)
        
class Author(models.Model):
    '''
    A class that represents the author of a blog post
    '''
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.username
    
    def get_absolute_url(self):
        return u'/%s/%d/%s/' % ('users', self.id, self.username)
        

class Post(models.Model):
    '''
    A holder for blog post information
    '''
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(Author)
    categories = models.ForeignKey(Category)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        category = self.categories;
        return u'/%s/%s/%s/%s/' % (self.categories.slug, self.created.year, self.created.month, self.slug)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
    
class Comment(models.Model):
    '''
    A class to hold comments for blog posts
    '''
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.post.title
    
    class Meta:
        ordering = ['created']