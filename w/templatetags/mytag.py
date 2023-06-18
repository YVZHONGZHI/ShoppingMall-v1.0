from w import models
from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth


register = template.Library()


@register.inclusion_tag('left_menu.html')
def left_menu(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    mall = user_obj.mall
    category_list = models.Category.objects.filter(mall=mall).annotate(count_num=Count('goods__pk')).values_list('name', 'count_num', 'pk')
    tag_list = models.Tag.objects.filter(mall=mall).annotate(count_num=Count('goods__pk')).values_list('name', 'count_num', 'pk')
    date_list = models.Goods.objects.filter(mall=mall).annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values_list('month', 'count_num')
    return locals()