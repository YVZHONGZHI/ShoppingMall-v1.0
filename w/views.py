import json

from w import models
from bs4 import BeautifulSoup
from django.db.models import F
from django.contrib import auth
from django.db import transaction
from django.http import JsonResponse
from w.myforms import MyRegForm, EndForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            return redirect('/home/')
        else:
            return redirect('/register/')
    return render(request, 'login.html')


def register(request):
    form_obj = MyRegForm()
    if request.method == 'POST':
        back_dic = {"code": 1000, 'msg': ''}
        form_obj = MyRegForm(request.POST)
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data
            clean_data.pop('confirm_password')
            file_obj = request.FILES.get('avatar')
            if file_obj:
                clean_data['avatar'] = file_obj
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 1001
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'register.html', locals())


def home(request):
    goods_queryset = models.Goods.objects.all()
    return render(request, 'home.html', locals())


@login_required
def vip(request):
    goods_list = models.Goods.objects.all()
    if request.method == 'POST':
        return redirect('/exhibit/')
    return render(request, 'vip.html', locals())


@login_required
def exhibit(request):
    form_obj = EndForm()
    goods_list = models.Goods.objects.all()
    if request.method == 'POST':
        back_dic = {"code": 1000, 'msg': ''}
        form_obj = EndForm(request.POST)
        if form_obj.is_valid():
            password = request.POST.get('password')
            if auth.authenticate(request, username=request.user, password=password):
                back_dic['password'] = password
                back_dic['msg'] = "暂  时  缺  货  ,  为  您  推  荐  其  它  产  品"
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = "账号密码错误!"
            return JsonResponse(back_dic)
        else:
            back_dic['code'] = 1002
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'exhibit.html', locals())


def site(request, username, **kwargs):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'errors.html')
    mall = user_obj.mall
    goods_list = models.Goods.objects.filter(mall=mall)
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            goods_list = goods_list.filter(category_id=param)
        elif condition == 'tag':
            goods_list = goods_list.filter(tags__id=param)
        else:
            year, month = param.split('-')
            goods_list = goods_list.filter(create_time__year=year, create_time__month=month)
    return render(request, 'site.html', locals())


def goods_detail(request, username, goods_id):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    mall = user_obj.mall
    goods_obj = models.Goods.objects.filter(mall__userinfo__username=username, pk=goods_id).first()
    if not goods_obj:
        return render(request, 'errors.html')
    comment_list = models.Comment.objects.filter(goods=goods_obj)
    return render(request, 'goods_detail.html', locals())


def set_password(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            is_right = request.user.check_password(old_password)
            if is_right:
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    back_dic['msg'] = '修改成功'
                else:
                    back_dic['code'] = 1001
                    back_dic['msg'] = '两次密码不一致'
            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '原密码错误'
        return JsonResponse(back_dic)


def set_avatar(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':
            file_obj = request.FILES.get('avatar')
            user_obj = request.user
            if file_obj:
                user_obj.avatar = file_obj
            else:
                user_obj.avatar = 'avatar/w.jpg'
            user_obj.save()
            back_dic['msg'] = '修改成功'
        return JsonResponse(back_dic)


@login_required
def backend(request):
    car_list = models.ShopCar.objects.filter(user=request.user)
    flow_list = models.Flow.objects.filter(user=request.user)
    goods_list = models.Goods.objects.filter(mall=request.user.mall)
    return render(request, 'backend/backend.html', locals())


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/home/')


def shop_car(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.user.is_authenticated:
            goods_id = request.POST.get('goods_id')
            goods_obj = models.Goods.objects.filter(pk=goods_id).first()
            if not goods_obj.mall.userinfo == request.user:
                is_click = models.ShopCar.objects.filter(user=request.user, goods=goods_obj)
                if not is_click:
                    back_dic['msg'] = '加入购物车成功'
                    models.ShopCar.objects.create(user=request.user, goods=goods_obj)
                else:
                    back_dic['code'] = 1001
                    back_dic['msg'] = '不能重复点击'
            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '自己不能点击'
        else:
            back_dic['code'] = 1003
            back_dic['msg'] = '<a href="/login/" style="text-decoration:none">请先登录</a>'
        return JsonResponse(back_dic)


def up_or_down(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.user.is_authenticated:
            goods_id = request.POST.get('goods_id')
            is_up = request.POST.get('is_up')
            is_up = json.loads(is_up)
            goods_obj = models.Goods.objects.filter(pk=goods_id).first()
            if not goods_obj.mall.userinfo == request.user:
                is_click = models.UpAndDown.objects.filter(user=request.user, goods=goods_obj)
                if not is_click:
                    if is_up:
                        models.Goods.objects.filter(pk=goods_id).update(up_num=F('up_num') + 1)
                        back_dic['msg'] = '点赞成功'
                    else:
                        models.Goods.objects.filter(pk=goods_id).update(down_num=F('down_num') + 1)
                        back_dic['msg'] = '点踩成功'
                    models.UpAndDown.objects.create(user=request.user, goods=goods_obj, is_up=is_up)
                else:
                    back_dic['code'] = 1001
                    back_dic['msg'] = '不能重复点击'
            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '自己不能点击'
        else:
            back_dic['code'] = 1003
            back_dic['msg'] = '<a href="/login/" style="text-decoration:none">请先登录</a>'
        return JsonResponse(back_dic)


def comment(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':
            if request.user.is_authenticated:
                goods_id = request.POST.get('goods_id')
                content = request.POST.get('content')
                parent_id = request.POST.get('parent_id')
                with transaction.atomic():
                    models.Goods.objects.filter(pk=goods_id).update(comment_num=F('comment_num') + 1)
                    models.Comment.objects.create(user=request.user, goods_id=goods_id, content=content, parent_id=parent_id)
                if parent_id:
                    content_time = models.Comment.objects.filter(user=request.user, goods_id=goods_id, content=content, parent_id=parent_id).first().content_time
                else:
                    content_time = models.Comment.objects.filter(user=request.user, goods_id=goods_id, content=content).first().content_time
                back_dic['msg'] = content_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = '<a href="/login/" style="text-decoration:none">请先登录</a>'
            return JsonResponse(back_dic)


def pay(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':
            goods_id = request.POST.get('goods_id')
            goods_obj = models.Goods.objects.filter(pk=goods_id).first()
            buy_user = models.UserInfo.objects.filter(username=request.user).first()
            if buy_user.balance >= goods_obj.shop_price:
                models.UserInfo.objects.filter(username=request.user).update(balance=F('balance') - goods_obj.shop_price)
                new_buy_user = models.UserInfo.objects.filter(username=request.user).first()
                models.Flow.objects.create(user=request.user, goods_id=goods_id, buy_num=1, balance_flow=new_buy_user.balance)
                models.ShopCar.objects.filter(user=request.user, goods_id=goods_id).delete()
                models.UserInfo.objects.filter(mall=goods_obj.mall_id).update(balance=F('balance') + goods_obj.shop_price)
                sell_user = models.UserInfo.objects.filter(mall=goods_obj.mall_id).first()
                models.Flow.objects.create(user=sell_user, goods_id=goods_id, sell_num=1, balance_flow=sell_user.balance)
                back_dic['msg'] = '支付成功'
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = '您的余额不足'
            return JsonResponse(back_dic)


def cancel(request):
    if request.is_ajax():
        back_dic = {"code": 1000, 'msg': ''}
        if request.method == 'POST':
            goods_id = request.POST.get('goods_id')
            models.ShopCar.objects.filter(user=request.user, goods_id=goods_id).delete()
            back_dic['msg'] = '取消订单成功'
            return JsonResponse(back_dic)


@login_required
def add_goods(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        shop_price = request.POST.get('shop_price')
        content = request.POST.get('content')
        file_obj = request.FILES.get('shop_picture')
        category_id = request.POST.get('category')
        tag_id_list = request.POST.getlist('tag')
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[0:130]
        if file_obj:
            goods_obj = models.Goods.objects.create(shop_name=shop_name, shop_price=shop_price, content=str(soup), shop_picture=file_obj, desc=desc, category_id=category_id, mall=request.user.mall)
        else:
            goods_obj = models.Goods.objects.create(shop_name=shop_name, shop_price=shop_price, content=str(soup), desc=desc, category_id=category_id, mall=request.user.mall)
        goods_obj_list = []
        for i in tag_id_list:
            tag_goods_obj = models.Goods2Tag(goods=goods_obj, tag_id=i)
            goods_obj_list.append(tag_goods_obj)
        models.Goods2Tag.objects.bulk_create(goods_obj_list)
        return redirect('/backend/')
    tag_list = models.Tag.objects.filter(mall=request.user.mall)
    category_list = models.Category.objects.filter(mall=request.user.mall)
    return render(request, 'backend/add_goods.html', locals())