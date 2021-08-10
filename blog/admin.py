from django.contrib import admin
from blog.models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)