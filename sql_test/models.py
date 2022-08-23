from django.db import models

# Create your models here.
class Article(models.Model):

    #資料庫中創建欄位
    title = models.CharField(max_length=30, default='my title')
    content = models.TextField(null=True)