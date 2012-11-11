from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from blog.models import Author, Category, Comment, Post
from blog.forms import AuthorForm, CategoryForm, CommentForm, PostForm

def add_author(request):
    '''
    Adds a blog author
    '''
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            author = Author.objects.get(username=form.cleaned_data['username'])
            return HttpResponseRedirect(reverse('blog.views.get_author',args=(author.id, author.username,)))
    else:
        form = AuthorForm()
    return render_to_response('form.html', {'form':form, 'action':'add_author'}, RequestContext(request))

def edit_author(request, id):
    '''
    Edit author information
    '''
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author_edited = form.save(commit=False)
            author.username = author_edited.username
            author.full_name = author_edited.full_name
            author.save()
        return HttpResponseRedirect(reverse('blog.views.get_author',args=(author.id, author.username,)))
    else:
        form = AuthorForm(instance=author)
    return render_to_response('form.html', {'form':form, 'action':'edit_author'}, RequestContext(request))

def get_author(request, id, username):
    '''
    Gets Author and returns author info and posts
    '''
    author = get_object_or_404(Author, id=id, username=username)
    posts = Post.objects.filter(author=author)
    return render_to_response('show_users.html', {'author':author, 'posts':posts}, RequestContext(request))

def add_category(request):
    '''
    Adds a new blog category
    '''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category = Category.objects.get(title=form.cleaned_data['title'])
            return HttpResponseRedirect(reverse('blog.views.get_category',args=(category.slug,)))
    else:
        form = CategoryForm()
    return render_to_response('form.html', {'form':form, 'action':'add_category'}, RequestContext(request))

def edit_category(request, id):
    '''
    Edits category information
    '''
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_edited = form.save(commit=False)
            category.title = category_edited.title
            category.description = category_edited.description
            category.save()
        return HttpResponseRedirect(reverse('blog.views.get_category',args=(category.slug,)))
    else:
        form = CategoryForm(instance=category)
    return render_to_response('form.html', {'form':form, 'action':'edit_category'}, RequestContext(request))

def get_category(request, slug):
    '''
    Gets Category and its related posts
    '''
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category)    
    return render_to_response('show_category.html', { 'category': category, 'posts': posts}, RequestContext(request))

def add_post(request):
    '''
    Adds a new post
    '''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            post = Post.objects.get(title=form.cleaned_data['title'])
            return HttpResponseRedirect(reverse('blog.views.get_post',args=(post.created.year, post.created.month, post.categories.slug,post.slug,)))
    else:
        form = PostForm()
    return render_to_response('form.html', {'form':form, 'action':'add_post'}, RequestContext(request))

def edit_post(request, id):
    '''
    Edits blog post
    '''
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_edited = form.save(commit=False)
            post.title = post_edited.title
            post.body = post_edited.body
            post.author = post_edited.author
            post.save()
        return HttpResponseRedirect(reverse('blog.views.get_post',args=(post.created.year, post.created.month, post.categories.slug,post.slug,)))
    else:
        form = PostForm(instance=post)
    return render_to_response('form.html', {'form': form, 'action':'edit_post'}, RequestContext(request))

def delete_post(request, id):
    '''
    Removes post from blog
    '''
    post = get_object_or_404(Post, id=id)
    for comment in post.comment_set.all():
        comment.delete()
    post.delete()
    return HttpResponseRedirect('/')

def delete_comment(request, id):
    '''
    Removes comment from blog post
    '''
    comment = get_object_or_404(Comment, id=id)
    post = comment.post
    comment.delete()
    return HttpResponseRedirect(reverse('blog.views.get_post',args=(post.created.year, post.created.month, post.categories.slug,post.slug,)))

def get_post(request, year, month, categories, slug):
    '''
    Gets post by category
    '''
    post = get_object_or_404(Post,slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render_to_response('show_post.html', {'post': post, 'form': form}, RequestContext(request))