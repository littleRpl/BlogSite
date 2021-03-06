from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PostManager(models.Manager):
    # 按日期归档统计
    def archive_date(self):
        archive_dict = {}
        for date in self.values('created_time'):
            pub_date = date['created_time'].strftime('%Y-%m')
            archive_dict[pub_date] = archive_dict.get(pub_date, 0) + 1

        return archive_dict




class Post(models.Model):
    title = models.CharField('标题',  max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    views = models.PositiveIntegerField('阅读量', default=0, editable=False)

    # comment_count = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 重写save，自动生成摘要
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将markdown文件渲染成html
        # strip_tags去掉html文本里的全部html标签
        # 从文本里摘出54个字符作为摘要
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])