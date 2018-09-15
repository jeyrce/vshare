from django.shortcuts import render
from django.views import View
from utils.page_breaker import pagebreaker
from file.models import File, FileType
from article.models import Article, Tag, Category
# Create your views here.

# 标签归档
class TagArchive(View):
    def get(self, request, tag_id, page_num=1):
        dic = {}
        tag_id, page_num = int(tag_id), int(page_num)
        dic['tag_'] = Tag.objects.get(is_delet=0, id=tag_id)
        queryset = Article.objects.filter(is_delet=0, tag_id=tag_id)
        dic['count'] = queryset.count()
        perpage = 30
        dic['page_articles'], dic['range_'], dic['num_pages'] = pagebreaker(queryset, page_num, perpage)
        return render(request, 'tag_archive.html', dic)


# 博文分类归档
class CateArchive(View):
    def get(self, request, cat_id, page_num=1):
        dic = {}
        cat_id, page_num = int(cat_id), int(page_num)
        dic['cat_'] = Category.objects.get(is_delet=0, id=cat_id)
        queryset = Article.objects.filter(is_delet=0, category_id=cat_id)
        dic['count'] = queryset.count()
        perpage = 30
        dic['page_articles'], dic['range_'], dic['num_pages'] = pagebreaker(queryset, page_num, perpage)
        return render(request, 'category_archive.html', dic)


# 文件归档
class FileArchive(View):
    def get(self, request, type_id, page_num=1):
        dic = {}
        type_id, page_num = int(type_id), int(page_num)
        dic['type_'] = FileType.objects.get(is_delet=0, id=type_id)
        queryset = File.objects.filter(is_delet=0, filetype_id=type_id)
        dic['count'] = queryset.count()
        perpage = 30
        dic['page_files'], dic['range_'], dic['num_pages'] = pagebreaker(queryset, page_num, perpage)
        return render(request, 'file_archive.html', dic)












