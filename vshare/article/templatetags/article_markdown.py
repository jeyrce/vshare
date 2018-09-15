# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-04-20
# purpose= 文章详情页支持markdown语法

from django.template import Library
import markdown2

register = Library()

@register.filter
def md(value):
    return markdown2.markdown(value)






if __name__ == '__main__':
    pass

