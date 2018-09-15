from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
from django.db.models import Q, F
from article.models import Article, Discussion
from utils.page_breaker import pagebreaker
from utils.getnow import now
# Create your views here.



class ArticleView(View):
    # 查看文章详情
    def get(self, request, article_id, page_num=0):
        num = int(page_num)
        a_id = int(article_id)
        article = Article.objects.get(id=a_id)
        if num == 0:
            # 文章浏览数加1，返回文章详情页
            try:
                Article.objects.filter(id=a_id).update(read=F('read')+1)
            except:
                pass
            return render(request, 'article_details.html', {'article': article})
        else:
            discussion = Discussion.objects.filter(Q(article_id=a_id) & Q(is_delet=0))
            per_page = 10
            page_discussion, range_, num_pages = pagebreaker(discussion, num, per_page)
            return render(request, 'article_discussion.html',{'article': article, 'page_discussion': page_discussion, 'range_': range_, 'num_pages': num_pages})

    # 假设被攻击
    def post(self, request):
        return render(request, 'Warning.html')

# 进行评论
class DiscussView(View):
    base_str = '''
    <script>
    alert("{}");
    window.location.href = '{}';
    </script>
    '''
    def get(self, request):
        return render(request, 'Warning.html')

    # 进行评论
    def post(self, request):
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        not_valid_str = DiscussView.base_str.format('内容不能为空！', '/article/details/{}/'.format(article_id))
        defeat_str = DiscussView.base_str.format('评论失败，稍后再试！', '/article/details/{}/'.format(article_id))
        # success_str = DiscussView.base_str.format('', '/article/details/{}/'.format(article_id))
        if not content:
            return HttpResponse(not_valid_str)
        try:
            # 写入数据库
            Discussion.objects.create(
                create_time=now(),
                content=content,
                article_id=article_id,
                user_id=user_id,
                is_delet=0
            )
            # F查询,帖子评论数加1
            Article.objects.filter(id=article_id).update(discuss=F('discuss')+1)
        except:
            return HttpResponse(defeat_str)
        else:
            return HttpResponseRedirect('/article/details/{}'.format(article_id))






