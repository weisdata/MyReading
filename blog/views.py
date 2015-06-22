from bs4 import BeautifulSoup
import re
import requests

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
#            from newspaper import Article
#            article = Article(url)
#            article.download()
#            print article.html
            r = requests.get(url)
            htmlSource = r.text
            soup = BeautifulSoup(htmlSource)
            title = soup.title.contents[0]

            all_meta = soup.find_all('meta')
            image = ''
            for element in str(all_meta).split('<'):
                if 'property="og:image' in element:
                    for img_li in re.findall('"([^"]*)"', element.split()[1]):
                        image = img_li
                        break
            text = ''
            form = PostForm({'title': title, 'text': text, 'image': image, 'link':url}) 
        else:
            form = PostForm() 

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
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