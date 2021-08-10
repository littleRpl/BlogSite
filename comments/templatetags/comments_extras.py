# -*- coding: utf-8 -*-
"""
-----------------------------------------------------
File Name:  comments_extra
Description:
Author:  rpl
Date:  2021-07-11 14:53
-----------------------------------------------------
Change Activity:  
    2021-07-11 14:53: 
"""
from django import template
from comments.forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()

    return {
         'form': form,
         'post': post
     }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count,
    }
