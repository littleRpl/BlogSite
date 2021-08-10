# -*- coding: utf-8 -*-
"""
-----------------------------------------------------
File Name:  forms
Description:  处理评论表单
Author:  rpl
Date:  2021-07-11 14:50
-----------------------------------------------------
Change Activity:
    2021-07-11 14:50:
"""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
