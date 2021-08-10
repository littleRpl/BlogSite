# -*- coding: utf-8 -*-
"""
-----------------------------------------------------
File Name:  blog_extras
Description:  存放自定义的模版标签代码
Author:  rpl
Date:  2021-07-10 20:52
-----------------------------------------------------
Change Activity:
    2021-07-10 20:52:
"""
from django import template
from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_post.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


# 归档模版标签
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):

    date_list = []
    date_dict = Post.objects.archive_date()
    for date, count in date_dict.items():
        year, month = date.split('-')
        date_list.append([year, month, count])

    return {
        'date_list': date_list,
    }


# 分类模版标签
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


# 标签云模版标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }