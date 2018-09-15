# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-03-30
# purpose= 登录user对象全局上下文


def get_user_by_account(user_account):
    from user_.models import User
    user = ''
    try:
        user = User.objects.get(account=user_account)
    except:
        pass
    return user


def has_user(request):
    # 查看session里面的user对象
    user_account = request.session.get('user')
    # print(user_account,'---------')
    user = get_user_by_account(user_account)
    # print(user,'===========')
    return {'user_': user}





if __name__ == '__main__':
    pass

