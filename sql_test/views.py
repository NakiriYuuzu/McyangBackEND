from django.shortcuts import render
# 頁面跳轉
from django.http import HttpResponseRedirect
from sql_test.models import Article
# Create your views here.

# 在瀏覽器中顯示我們想要顯示的資料
def index(request):
    articles = Article.objects.all()
    return render(request,'index.html',{'articles':articles})

# 刪除資料
def delete(request,article_id):
    try:
        Article.objects.get(id=article_id).delete()
    except Exception:
        print('異常處理')
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})

def get_id(request):
    article = Article.objects.get(id=id)
    return render(request,'update.html',{'article':article})

#更新資料
def update(request):
    id = request.POST.get('id')
    article = Article.objects.get(id=id)
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()

    return HttpResponseRedirect('/')


def login(request):
    return None