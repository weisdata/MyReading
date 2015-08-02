from newspaper import Article
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from .forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

def post_list(request):
    if request.method == 'GET':
    	posts = Post.objects.filter(author_id=request.user.id).order_by('-published_date')
        me = User.objects.get(username='weisdata')
        public_posts = Post.objects.filter(author=me).order_by('-published_date')
    	return render(request, 'blog/post_list.html',  {'posts': posts, 'public_posts': public_posts})
    elif request.method == 'POST':
        url = request.POST.get('url-input', '')
        if request.user.is_active:
            # query parameter -> ?url
            return redirect('/post/new/?url=%s' % url)
        else:
            return redirect('blog.views.register')

def post_delete(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            return render(request, 'blog/post_delete.html', {'post': post})
    elif request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
        return redirect('/', pk=post.pk)
    else:
        raise Http404()

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    me = User.objects.get(username='weisdata')
    if post.author == request.user:
        return render(request, 'blog/post_detail.html', {'post': post})
    elif post.author == me:
        public_posts = Post.objects.filter(author=me).order_by('-published_date')
        post = get_object_or_404(public_posts, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
    else:
        raise Http404()


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    elif request.method == 'GET':
        url = request.GET.get('url', '')
               
        if len(url) > 5:
            article = Article(url, language='en')
            article.download()
            article.parse()
            article.nlp()
            image = article.top_image
            summary = article.summary.replace('\n', ' ').replace(u'\u2019',"\'")
            title = article.title.replace(u'\u2019',"\'")
            source = url.split('//')[1].split('/')[0].replace('www.','')
            status = 'UD'
            form = PostForm({'title': title, 'summary': summary, 'image': image, 'link':url, 'source':source, 'status':status,}) 
        else:
            form = PostForm() 

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author_id == request.user.id:
        post.delete_url = '/blog/post/' + str(post.pk) + '/delete' 
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        raise Http404()

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(request,
            'blog/register.html',
            {'user_form': user_form, 'registered': registered} )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your MyReading account is disabled.")
        else:
            return HttpResponse("Your username and password didn't match. Try Aagin!")
    else:
        return render(request, 'blog/login.html', {})
        
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response







