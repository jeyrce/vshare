from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
# from django import forms
from . import models
import re
from utils.getnow import now
from utils.page_breaker import pagebreaker
from uuid import uuid4
from article.models import Article, Tag, Category
from file.models import File
# Create your views here.


class UserCenter(View):
    def get_hello(self):
        from utils.getnow import this_hour
        hello = '你好！'
        hour = int(this_hour())
        if hour in range(5, 8):
            hello = '早上好！一日之计在于晨, 早起的鸟儿有虫吃！'
        elif hour in range(8, 11):
            hello = '上午好！神清气爽, 干劲十足！'
        elif hour in range(11, 13):
            hello = '中午好！休息一下, 看看博客也不错哦！'
        elif hour in range(13, 16):
            hello = '下午好！午后时光, 是否困倦呢？去逛逛吧！'
        elif hour in range(16, 18):
            hello = '黄昏时分, 收拾一下心情，准备下班！'
        elif hour in range(18, 22):
            hello = '晚上好，吃过晚饭往沙发一趟，美滋滋！'
        elif hour in range(22, 24) or hour in range(0, 2):
            hello = '夜深了，是什么让你思绪万千无法入眠呢？不如写个博客倾吐一下吧！'
        else:
            hello = '凌晨啦！怎么还不睡，要注意保重身体呀！'
        return hello
    # 获取最近的动态
    def get_recent_states(self, user):
        queryset_arti = Article.objects.filter(is_delet=0, author_id=user.id).order_by('-id')
        queryset_file = File.objects.filter(is_delet=0, user_id=user.id).order_by('-id')
        recent_artis, range_, page_nums = pagebreaker(queryset_arti)
        recent_files, range_, page_nums = pagebreaker(queryset_file)
        return recent_artis, recent_files
    # 展示个人信息，发过的文章，上传的文件等
    def get(self, request):
        act = request.GET.get('act', None)
        dic = {}
        dic['hello'] = self.get_hello()
        account = request.session.get('user', '')
        try:
            find_user = models.User.objects.get(account=account, is_delet=0)
        except:
            return HttpResponse('<h1>你的账户已被冻结或注销！</h1>')
        if act == 'addtip':
            # 修改添加签名
            return render(request, 'tipform.html', dic)
        elif act == 'files':
            # 文件展示
            page_num = int(request.GET.get('page_num', 1))
            queryset = File.objects.filter(is_delet=0, user_id=find_user.id).order_by('-id')
            perpage = 30
            dic['count'] = queryset.count()
            files, range_, numpages = pagebreaker(queryset, page_num, perpage)
            dic['page_files'], dic['range_'], dic['num_pages'] = files, range_, numpages
            return render(request, 'userfiles.html', dic)
        elif act == 'articles':
            # 博客展示
            page_num = int(request.GET.get('page_num', 1))
            queryset = Article.objects.filter(is_delet=0, author_id=find_user.id).order_by('-id')
            perpage = 30
            dic['count'] = queryset.count()
            articles, range_, numpages = pagebreaker(queryset, page_num, perpage)
            dic['articles'], dic['range_'], dic['num_pages'] = articles, range_, numpages
            return render(request, 'userarticles.html', dic)
        else:
            arti_count = Article.objects.filter(is_delet=0, author_id=find_user.id).count()
            file_count = File.objects.filter(is_delet=0, user_id=find_user.id).count()
            dic['file_count'] = file_count
            dic['arti_count'] = arti_count
            dic['f_user'] = find_user
            dic['recent_articles'], dic['recent_files'] = self.get_recent_states(find_user)
            return render(request, 'usercenter.html', dic)


    def post(self, request):
        act = request.POST.get('act', None)
        if act == 'addtip':
            u_id = request.POST.get('u_id')
            new_tip = request.POST.get('new_tip')
            try:
                models.User.objects.filter(id=u_id).update(tip=new_tip)
            except:
                pass
        return HttpResponseRedirect('/user_/usercenter')

# 别人观看到的关于个人的信息
class UserDetails(View):
    def get(self, request, user_id):
        act = request.GET.get('act')
        dic = {}
        user_id = int(user_id)
        try:
            f_user = models.User.objects.get(id=user_id)
        except:
            return HttpResponse('<h1>此用户已经被冻结或者封禁！</h1>')
        dic['f_user'] = f_user
        queryset_arti = Article.objects.filter(is_delet=0, author_id=f_user.id)
        queryset_file = File.objects.filter(is_delet=0, user_id=f_user.id)
        dic['arti_count'] = queryset_arti.count()
        dic['file_count'] = queryset_file.count()
        dic['recent_articles'], range_, num_pages = pagebreaker(queryset_arti)
        dic['recent_files'], range_, num_pages = pagebreaker(queryset_file)
        if act == 'articles':
            page_num = int(request.GET.get('page_num', 1))
            queryset = Article.objects.filter(is_delet=0, author_id=f_user.id).order_by('-id')
            perpage = 30
            dic['count'] = queryset.count()
            articles, range_, numpages = pagebreaker(queryset, page_num, perpage)
            dic['articles'], dic['range_'], dic['num_pages'] = articles, range_, numpages
            return render(request, 'x_userarticles.html', dic)
        elif act == 'files':
            page_num = int(request.GET.get('page_num', 1))
            queryset = File.objects.filter(is_delet=0, user_id=f_user.id).order_by('-id')
            perpage = 30
            dic['count'] = queryset.count()
            files, range_, numpages = pagebreaker(queryset, page_num, perpage)
            dic['page_files'], dic['range_'], dic['num_pages'] = files, range_, numpages
            return render(request, 'x_userfiles.html', dic)
        else:
            return render(request, 'userdetails.html', dic)

    def post(self, request):
        return render(request, 'Warning.html')

# 登录表单发放以及验证
class Login(View):
    str_base = '''
    <script>
    alert("{}");
    window.location.href = '/user_/{}';
    </script>
    '''
    str_base2 = '''
    <script>
    alert("{}");
    window.location.href = '{}';
    </script>
    '''
    str_success = str_base2.format('登录成功！', '/')
    str_defeat = str_base.format('登录失败,密码不正确！如果你忘记了密码，可以点击右下角<忘记密码>进行找回。', 'login')
    str_user_not_exited = str_base.format('登录失败,用户名不存在,请前去注册！', 'regist')
    # 用户存在校验
    def _is_user_existed(self, account):
        if models.User.objects.filter(account=account).count() > 0:
            return True
        else:
            return False
    # 生成session_id
    @staticmethod
    def get_session_id():
        return uuid4().hex

    # 登陆表单
    def get(self, request):
        refer_url = request.META.get('HTTP_REFERER', '/')
        # print(request.META,'\n')
        # 取得登陆前要去的url, 没有则默认首页
        if refer_url.endswith('/user_/regist') or refer_url.endswith('/user_/login'):
            refer_url = '/'
        request.session['refer_url'] = refer_url
        # print(refer_url)
        return render(request, 'login.html')

    # 校验登陆信息
    def post(self, request):
        '''
        提取请求信息和数据库进行验证
        根据情况返回个人中心，注册，登录等页面以及提示信息
        '''
        # 表单提交上来的信息
        account = request.POST.get('account', '')
        pwd = request.POST.get('pwd', '')
        if self._is_user_existed(account):
            try:
                user = models.User.objects.get(account=account, pwd=pwd)
            except Exception:
                return HttpResponse(Login.str_defeat)
            else:
                # 成功了重定向,设置好 session  cookie
                # session_id = self.get_session_id()
                session_id = 'user'
                request.session[session_id] = user.account
                refer_url = request.session.get('refer_url', '/')
                return HttpResponseRedirect(refer_url)
        else:
            return HttpResponse(Login.str_user_not_exited)
# 注册
class Regist(View):
    str_user_over = '''
        < script >
        alert("感谢你对本社区的亲睐，目前本站会员数已经达到上限，尚未开放新的名额，请过段时间再来尝试！");
        window.location.href = '/user_/regist';
        < / script >
    '''
    base_str = '''
        <script>
        alert("{}");
        window.location.href = '/user_/regist';
        </script>
    '''
    str_00 = '''
        <script>
        alert("注册成功, 请牢记你的账户和密码({},{})");
        window.location.href = '/user_/login';
        </script>
    '''
    str_01 = base_str.format('账号只能是数字字母下划线组合，并且首位不可是数字，长度2~20')
    str_02 = base_str.format('密码只能是数字字母下划线组合，长度6~20')
    str_03 = base_str.format('问题长度不对，合法长度2~20')
    str_04 = base_str.format('答案长度不对，合法长度2~20')
    str_05 = base_str.format('手机号码不合法，请重新填写')
    str_06 = base_str.format('签名过长，最大长度为40字符')
    str_07 = base_str.format('未知错误，请稍后再试')
    str_08 = base_str.format('此账号已经存在!')
    pwd_is_not_sure_pwd = base_str.format('两次密码不一致！')
    # 账号格式校验
    def _is_account_valid(self, account):
        result = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{1,19}$', account)
        if result:
            return True
        else:
            return False
    # 密码格式校验
    def _is_pwd_valid(self, pwd):
        result = re.match(r'^[a-zA-Z0-9_]{6,20}$', pwd)
        if result:
            return True
        else:
            return False
    # 确认密码和密码一致性
    def _is_sure_pwd(self, pwd, sure_pwd):
        if pwd == sure_pwd:
            return True
        else:
            return False
    # 密保问题格式校验
    def _is_answer_valid(self, answer):
        result = re.match(r'^.{2,20}$', answer)
        if result:
            return True
        else:
            return False
    def _is_question_valid(self, question):
        result = re.match(r'^.{2,20}$', question)
        if result:
            return True
        else:
            return False
    def _is_phone_valid(self, phone):
        result = re.match(r'^1[0-9]{10}$', phone)
        if result:
            return True
        else:
            return False
    def _is_tip_valid(self, tip):
        result = re.match(r'^.{,40}$', tip)
        if result:
            return True
        else:
            return False
    def _is_account_exited(self, account):
        db_account = models.User.objects.filter(account=account,is_delet=0).count()
        if db_account > 0:
            return True
        else:
            return False

    # 表单下发
    def get(self, request):
        return render(request, 'regist.html')

    # 写入数据库，返回提示
    def post(self, request):
        from  vshare.settings import MAX_USER_SIZE
        # 会员数上限
        if models.User.objects.filter(is_delet=0).count() > MAX_USER_SIZE:
            return HttpResponse(Regist.str_user_over)
        account = request.POST.get('account', '')
        pwd = request.POST.get('pwd', '')
        sure_pwd = request.POST.get('sure_pwd', '')
        answer = request.POST.get('answer', '')
        question = request.POST.get('question', '')
        phone = request.POST.get('phone', '')
        tip = request.POST.get('tip', '')
        modified = now()
        successful_str = Regist.str_00.format(account, pwd)
        if not self._is_account_valid(account):
            # print(Regist.str_01)
            return HttpResponse(Regist.str_01)
        elif not self._is_pwd_valid(pwd):
            return HttpResponse(Regist.str_02)
        elif not self._is_sure_pwd(pwd, sure_pwd):
            return HttpResponse(Regist.pwd_is_not_sure_pwd)
        elif not self._is_question_valid(question):
            return HttpResponse(Regist.str_03)
        elif not self._is_answer_valid(answer):
            return HttpResponse(Regist.str_04)
        if phone:
            if not self._is_phone_valid(phone):
                return HttpResponse(Regist.str_05)
        if tip:
            if not self._is_tip_valid(tip):
                return HttpResponse(Regist.str_06)
        # 判断账号是否已经存在
        if self._is_account_exited(account):
            return HttpResponse(Regist.str_08)
        try:
            # 存入数据库
            models.User.objects.create(
                account=account,
                pwd=pwd,
                question=question,
                answer=answer,
                phone=phone,
                tip=tip,
                modified=modified,
                is_delet=0
            )
        except:
            return HttpResponse(Regist.str_07)
        else:
            return HttpResponse(successful_str)

# 注销登录
class Logout(View):
    def get(self, request):
        # 删除user, session, cookie,返回首页
        if 'user' in request.session:
            del request.session['user']
        return HttpResponseRedirect(redirect_to='/')

# 安全中心, 修改密码，找回密码
class SecureCenter(View):
    def get(self, request):
        return render(request, 'securecenter.html')

# from DjangoUeditor.forms import UEditorField, UEditorModelForm
#
# class ArticleForm(UEditorModelForm):
#     Description = UEditorField(u"文章正文", height=300, width=1000, default=u'', blank=True, imagePath="uploads/blog/images/",
#                            toolbars='besttome', filePath='uploads/blog/files/')
# 发表文章
class WriteArticle(View):
    def get(self, request):
        # 查出当前可以选的分类，标签
        usable_categories = Category.objects.filter(is_delet=0)
        usable_tags = Tag.objects.filter(is_delet=0)
        dic = {'u_cats': usable_categories, 'u_tags': usable_tags}
        # dic['form'] = ArticleForm()
        return render(request, 'article_form.html', dic)

    def post(self, request):
        defeat = "<script>alert('出现错误，稍后再试！');window.location.href='/';</script>"
        user_id = request.POST.get('user_id', '')
        title = request.POST.get('title', '')
        cat = request.POST.get('my_category', '')
        tag = request.POST.get('my_tag', '')
        cont = request.POST.get('content', '')
        # 数据库写入，返回首页
        a_id = request.POST.get('a_id', None)
        if  not a_id:
            try:
                Article.objects.create(
                    title=title,
                    create_time=now(),
                    content=cont,
                    read=0,
                    discuss=0,
                    is_delet=0,
                    author_id=user_id,
                    category_id=cat,
                    tag_id=tag
                )
            except:
                return HttpResponse(defeat)
        else:
            try:
                Article.objects.filter(id=a_id).update(
                    title=title,
                    create_time=now(),
                    content=cont,
                    read=0,
                    discuss=0,
                    is_delet=0,
                    author_id=user_id,
                    category_id=cat,
                    tag_id=tag
                )
            except:
                return HttpResponse(defeat)
        return HttpResponseRedirect('/')
# 用户修改密码
class ModifyPwd(View):
    base_str = '''
    <script>alert('{}');window.location.href = '{}';</script>
    '''
    pwd_wrong = base_str.format('密码验证错误！', '/user_/cpwd')
    pwd_not_sure = base_str.format('两次密码不一致！', '/user_/cpwd')
    pwd_not_valid = base_str.format('密码只能是数字字母下划线组合，长度6~20', '/user_/cpwd')
    def get(self, request):
        return render(request, 'cpwd.html')

    def post(self, request):
        user_id = request.POST.get('user_id', '')
        pwd = request.POST.get('pwd', '')
        new_pwd = request.POST.get('new_pwd', '')
        sure_pwd = request.POST.get('sure_pwd', '')
        user = models.User.objects.get(id=user_id)
        if user.pwd != pwd:
            return HttpResponse(ModifyPwd.pwd_wrong)
        if new_pwd != sure_pwd:
            return HttpResponse(ModifyPwd.pwd_not_sure)
        if not self._is_pwd_valid(new_pwd):
            return HttpResponse(ModifyPwd.pwd_not_valid)
        try:
            models.User.objects.filter(id=user.id).update(
                pwd=new_pwd,
                modified=now()
            )
        except:
            pass
        # 修改成功，注销当前登录
        return HttpResponseRedirect('/user_/logout')
    # 密码格式校验
    def _is_pwd_valid(self, pwd):
        result = re.match(r'^[a-zA-Z0-9_]{6,20}$', pwd)
        if result:
            return True
        else:
            return False

# 找回密码
class FindPwd(View):
    base_str = '''
    <script>alert('{}');window.location.href = '{}';</script>
    '''
    pwd_not_sure = base_str.format('两次密码不一致！', '/user_/findpwd?account={}')
    answer_descorrect = base_str.format('密保验证失败！', '/user_/findpwd?account={}')
    find_success = base_str.format('找回成功， 请牢记你的密码:{}', '/user_/login')
    def get(self, request):
        account = request.GET.get('account', '')
        if account:
            request.session['account'] = account
            try:
                user = models.User.objects.get(account=account, is_delet=0)
            except:
                user = None
            return render(request, 'findpwd.html', {'find_user': user})
        return render(request, 'findpwd.html')

    def post(self, request):
        user_id = request.POST.get('user_id', '')
        form_answer = request.POST.get('answer', '')
        new_pwd = request.POST.get('new_pwd', '')
        sure_pwd = request.POST.get('sure_pwd', '')
        account = request.session.get('account', '')
        if new_pwd != sure_pwd:
            return HttpResponse(FindPwd.pwd_not_sure.format(account))
        if self.answer_is_descorrect(form_answer, user_id):
            return HttpResponse(FindPwd.answer_descorrect.format(account))
        return HttpResponse(FindPwd.find_success.format(new_pwd))
    # 校验答案
    def answer_is_descorrect(self, form_answer, user_id):
        if models.User.objects.get(id=user_id).answer == form_answer:
            return False
        return True
# 更改密保
class ModifyPwdSafe(View):
    base_str = '''
    <script>alert('{}');window.location.href = '{}';</script>
    '''
    field_not_valid = base_str.format('问题和答案长度应该为2~20！', '/user_/cpwdsafe')
    not_sure_answer = base_str.format('两次答案不一致！', '/user_/cpwdsafe')
    defeat = base_str.format('修改失败, 稍后再试！', '/')
    def get(self, request):
        answer = request.GET.get('answer', '')
        user_id = request.GET.get('user_id', None)
        # print(user_id)
        result = False
        try:
            user = models.User.objects.get(id=user_id)
        except:
            user = None
        if user:
            result = (user.answer == answer)
            # print(result)
        return render(request, 'cpwdsafe.html', {'result': result})

    def post(self, request):
        user_id = request.POST.get('user_id', '')
        new_question = request.POST.get('new_question', '')
        new_answer = request.POST.get('new_answer', '')
        sure_answer = request.POST.get('sure_answer', '')
        if not self.is_length_valid(new_question, new_answer):
            return HttpResponse(ModifyPwdSafe.field_not_valid)
        if new_answer != sure_answer:
            return HttpResponse(ModifyPwdSafe.not_sure_answer)
        # 修改数据库
        try:
            models.User.objects.filter(id=user_id).update(
                question=new_question,
                answer=new_answer,
                modified=now()
            )
        except:
            return HttpResponse(ModifyPwdSafe.defeat)
        return HttpResponseRedirect('/')

    # 问题答案长度验证
    def is_length_valid(self, *strs):
        for str_ in strs:
            if len(str_) <2 or len(str_) > 20:
                return False
        return True

# 删除在此完成，修改在write覆盖
class ChangeArt(View):

    def get(self, request, f_id=-1):
        from user_.models import User
        user_account = request.session.get('user', '')
        refer_url = request.META.get('HTTP_REFERER', '/')
        # print(refer_url)
        act = request.GET.get('act', '')
        try:
            u_id = User.objects.get(account=user_account).id
            article = Article.objects.get(id=f_id)
            if u_id != article.author_id:
                return HttpResponseRedirect(refer_url)
            if act == 'del':
                try:
                    Article.objects.filter(id=f_id).update(is_delet=1)
                except:
                    pass
            elif act == 'mod':
                try:
                    article = Article.objects.get(id=f_id)
                except:
                    return HttpResponse(status=500)
                else:
                    usable_categories = Category.objects.filter(is_delet=0)
                    usable_tags = Tag.objects.filter(is_delet=0)
                    dic = {'u_cats': usable_categories, 'u_tags': usable_tags, 'article': article}
                    return render(request, 'mod_article.html', dic)
        except:
            pass
        return HttpResponseRedirect(refer_url)

    def post(self, request):
        return render(request, 'Warning.html')









