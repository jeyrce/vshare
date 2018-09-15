# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-05-05
# purpose= 归档信息全局上下文


from article.models import Article, Tag, Category
from file.models import FileType, File
from utils.page_breaker import pagebreaker


def archive_info(request):
    info = {'categories':{}, 'tags': {}, 'types': {}}
    # 博文分类
    categories = Category.objects.filter(is_delet=0)
    info['categories'] = []
    for category in categories:
        count = Article.objects.filter(is_delet=0, category_id=category.id).count()
        info['categories'].append((category, count))
    # print(info)
    # 博文标签
    tags = Tag.objects.filter(is_delet=0)
    info['tags'] = []
    for tag in tags:
        count = Article.objects.filter(is_delet=0, tag_id=tag.id).count()
        info['tags'].append((tag, count))
    # 文件分类
    types = FileType.objects.filter(is_delet=0)
    info['types'] = []
    for type_ in types:
        count = File.objects.filter(is_delet=0, filetype_id=type_.id).count()
        info['types'].append((type_, count))
    # top 10 博客，按评论数
    info['top_10_arti'] = []
    queryset_1 = Article.objects.filter(is_delet=0).order_by('-read')
    articles, range_1, pages_1 = pagebreaker(queryset_1)
    info['top_10_arti'] = articles
    # top 10 文件，按下载量
    info['top_10_file'] = []
    queryset_2 = File.objects.order_by('-download').filter(is_delet=0)
    files, range_2, pages_2 = pagebreaker(queryset_2)
    info['top_10_file'] = files
    return info













if __name__ == '__main__':
    pass

