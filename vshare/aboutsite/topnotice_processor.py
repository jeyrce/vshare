# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 201x-xx-xx 
# purpose= 置顶公告全局模板上下文

from aboutsite.models import TopNotice




# 查出最近的一条作为全局上下文
def top_notice(request):
    notice = TopNotice.get_most_recent_one()
    return {'top_notice': notice}







if __name__ == '__main__':
    pass

