from django.shortcuts import render, HttpResponse
from django.views import View
# from django.core.paginator import Paginator
from article.models import *
from aboutsite.models import VisitDocument
from utils import getnow
# Create your views here.


class MainPage(View):
    # 网站首页的访问记录
    def __doc_for_first_vist_mainpage(self, request, num):
        host = '0.0.0.0'
        try:
        # 获取主机地址，- 开头表示使用了ip代理
            if num == 1:
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    host = '-' + request.META['HTTP_X_FORWARDED_FOR']
                elif 'REMOTE_ADDR' in request.META:
                    host = request.META['REMOTE_ADDR']
            else:
                return
        except Exception as e:
            # print(e)
            return
        else:
            visit_time = getnow.now()
            is_delet = 0
        try:
            VisitDocument.objects.create(
                host = host,
                visit_time = visit_time,
                is_delet = is_delet,
            )
        except Exception as e2:
            # print(e2)
            return

    def get_article_by_num(self, num):
        from utils.page_breaker import pagebreaker
        query_set = Article.objects.order_by('-id').filter(is_delet=0)
        num = int(num)
        perpage = 7
        return pagebreaker(query_set, num, perpage)

    # 访问首页
    def get(self, request, num=1):
        # 写入首页访问记录
        self.__doc_for_first_vist_mainpage(request, num)
        # 寻找cookie，查看登陆信息，返回用户的id
        pass
        # 文章分页显示，
        articles, range_, num_pages = self.get_article_by_num(num)
        # 右侧的显示
        pass
        return render(request, 'mainpage.html', {'articles': articles, 'range_': range_, 'num_pages': num_pages})

    def post(self, request):

        return render(request, 'Warning.html')

# 全文搜索
class SearchView(View):
    def post(self, request):
        return render(request, 'expected.html')

    def get(self, request):

        return render(request, 'expected.html')





