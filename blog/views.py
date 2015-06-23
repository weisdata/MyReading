from newspaper import Article
import re

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    if request.method == 'GET':
    	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    	return render(request, 'blog/post_list.html', {'posts': posts})
    elif request.method == 'POST':
        url = request.POST.get('url-input', '')
        # query parameter -> ?url
        return redirect('/post/new/?url=%s' % url)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
            summary = article.summary.replace('\n', ' ')
            title = article.title
            source = url.split('//')[1].split('/')[0].replace('www.','')

            form = PostForm({'title': title, 'summary': summary, 'image': image, 'link':url, 'source':source, }) 
        else:
            form = PostForm() 

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
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