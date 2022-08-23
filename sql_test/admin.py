from django.contrib import admin
from sql_test.models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','content']

# 註冊後台管理
admin.site.register(Article,ArticleAdmin)
