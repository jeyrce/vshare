# coding = utf-8
# env    = python3.5.2
# author = lujianxin
# time   = 2018-05-13
# purpose= 自定义文章发布表单

from django import forms
from article.models import Article
from DjangoUeditor.forms import UEditorModelForm


class ArticleForm(UEditorModelForm):
    class META:
        module = Article


if __name__ == '__main__':
    pass

