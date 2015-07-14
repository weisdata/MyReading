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


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author_id == request.user.id:
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
            print source
            status = 'UD'
            form = PostForm({'title': title, 'summary': summary, 'image': image, 'link':url, 'source':source, 'status':status,}) 
        else:
            form = PostForm() 

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author_id == request.user.id:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            print form
            if form.is_valid():
                post = form.save(commit=False)
                print post.title
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        raise Http404
    

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
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Your username and password do not match. Try Again!")

    else:
        return render(request, 'blog/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def custom_404(request):
    return render_to_response('404.html')







