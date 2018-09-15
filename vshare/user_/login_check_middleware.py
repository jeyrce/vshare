# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-04-29
# purpose= 登录状态验证中间件

from vshare.settings import LOGIN_AUTH_LIST
from django.http import HttpResponse

# 已登陆则正常请求，否则提示登录，重定向登录页面
class LoginCheck(object):
    redirect_str = '''
    <script>
    alert("检测到您并未登录，此功能需要登录后方可使用，请前去登录！");
    window.location.href = '/user_/login';
    </script>
    '''
    # 保存请求内容
    def __init__(self, get_response):
        self.get_response = get_response

    # 重写__call__,对象被创建时执行下面的逻辑
    def __call__(self, request, *args, **kwargs):
        # print(request.path)
        if request.path in LOGIN_AUTH_LIST:
            if not request.session.get('user'):
                return HttpResponse(LoginCheck.redirect_str)
        # 验证通过则执行刚才的请求，该干啥干啥
        return self.get_response(request, *args, **kwargs)




if __name__ == '__main__':
    pass

