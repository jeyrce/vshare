from django.shortcuts import render
from django.views import View
# from django.db.models import Q
from utils.page_breaker import pagebreaker
from django.shortcuts import HttpResponse,redirect
from django.http import JsonResponse
# Create your views here.

from aboutsite.models import MsgBoard
from utils import code,getnow
# 网站留言板
class MsgBoardView(View):
    # 查询最近的num条
    def __get_recent_by_num(self, perpage=10):
        query_set = MsgBoard.objects.order_by('-id').filter(is_delet=0)
        per_page = int(perpage)
        num = 1
        return pagebreaker(query_set, num, per_page)


    # 进入留言板页面，此处只显示最近的10条因此不做分页处理
    # 但是利用分页查询最近的10条记录
    def get(self, request):
        msgs = self.__get_recent_by_num()[0]
        return render(request, 'msgboard.html', {'msgs': msgs})
    # 进行留言
    def post(self, request):
        host = request.META.get('REMOTE_ADDR', '0.0.0.0')
        # 删除验证码的session
        try:
            del request.session[host]
        except:
            pass
        base_str = '''
        <script>
        alert("{}");
        window.location.href = '/aboutsite/msgboard';
        </script>
        '''
        success_code = '<script>window.location.href="/aboutsite/msgboard";</script>'
        defeat_code = base_str.format('留言失败，可能是留言过长导致的，请稍后再试！')
        empty_content = base_str.format('留言内容不能为空！')
        # print(success_code, defeat_code)
        # 留言写入数据库
        nickname = request.POST.get('nickname', None)
        email = request.POST.get('email', None)
        content = request.POST.get('content', None)
        if content:
            pass
        else:
            return HttpResponse(empty_content)
        create_time = getnow.now()
        is_delet = 0
        try:
            MsgBoard.objects.create(
                nickname=nickname,
                create_time=create_time,
                content=content,
                email=email,
                is_delet=is_delet
            )
        except Exception as e:
            return JsonResponse({'result_info': defeat_code})
        else:
            return JsonResponse({'result_info': success_code})

# 生成验证码
class Code(View):
    def get(self, request):
        host = request.META.get('REMOTE_ADDR', '0.0.0.0')
        img, str = code.gene_code()
        # print(str, '--------------')
        request.session[host] = str
        # 返回去一张渲染后的验证码图片
        return HttpResponse(img, content_type='image/png')

# 校验验证码
class CheckCode(View):
    def get(self, request):
        host = request.META.get('REMOTE_ADDR', '0.0.0.0')
        code = request.GET.get('confirmcode', None)
        if code == '-----':
            result = True
        else:
            # 从数据库获取sessioncode，然后时间设置为负让他过期
            scode = request.session.get(host, '-1')
            result = code == scode
        return JsonResponse({'checkFlag': result})

# 关于信息,静态页面
class MyInfoView(View):
    def get(self, request):
        # return HttpResponse(status=403)
        # return HttpResponse(status=500)
        return render(request, 'myinfo.html')

    def post(self, request):
        return render(request, 'Warning.html')
