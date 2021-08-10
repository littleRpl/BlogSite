from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from blog.models import Post, Category, Tag

import markdown
from markdown.extensions.toc import TocExtension
import re


# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-created_time')  # - 表示逆序

    return render(request, 'blog/index.html', context={
        'post_list': post_list,

    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 统计阅读量
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),  # 美化标题锚点 .../#_1
    ])
    post.body = md.convert(post.body)

    # 处理空toc
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={
        'post': post,
    })


def archives(request, year, month):

    # Python中调用属性的方式通常是created_time.year,
    # 但是这里作为方法的参数列表,django把点替换成了两个下划线，即created_time__year
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)

    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def bg(request):
    return render(request, 'blog/full-width.html')