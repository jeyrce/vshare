# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-04-16
# purpose= 通用分页逻辑，

from django.core.paginator import Paginator

# 分页方法
def pagebreaker(queryset, num=1, perpage=10):
    '''
    :param queryset: 要进行分页的数据集合
    :param num: 分页后返回页码
    :param perpage: 每页多少条记录
    :return: 对应num的页内容，分页区间,总页数
    '''
    num = int(num)
    page_datas = Paginator(queryset, per_page=perpage)
    # 控制当前页不可越界
    if num <= 0:
        num = 1
    if num > page_datas.num_pages:
        num = page_datas.num_pages
    # 生成前端需要的页码数
    # 起始数, 下图中的10表示一个分页条最多显示10个
    start = ((num - 1) // 10) * 10 + 1
    # 末尾数
    end = start + 10
    # 判断end是否越界
    if end > page_datas.num_pages:
        end = page_datas.num_pages
    return page_datas.page(num), range(start, end + 1), page_datas.num_pages


if __name__ == '__main__':
    pass

