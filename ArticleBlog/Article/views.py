from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Article.models import *
import hashlib
from django.core.paginator import Paginator
# Create your views here.
#密码加密
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result
#注册
def register(requset):
    if requset.method=="POST":
        error_msg=''
        email=requset.POST.get('email')
        password=requset.POST.get("password")
        if email:
            #判断邮箱是否存在
            loginuser=Author.objects.filter(email=email).first()
            if not loginuser:
                #不存在 写库
                user=Author()
                user.email=email
                user.name=email
                user.password=setPassword(password)
                user.user_type=0
                user.save()
            else:
                error_msg="邮箱已经被注册，请登录"
        else:
            error_msg="邮箱不可以为空"
    return render(requset,'article/register.html',locals())
#登录装饰器
def LoginVaild(func):
    #1.获取cookie中username和email
    #2.判断username和email
    #3.如果成功 跳转
    #4.如果失败 login.html
    def inner(request,*args,**kwargs):
        username=request.COOKIES.get('username')

        #获取session
        session_username=request.session.get('username')
        if username and session_username and username==session_username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Article/login/')
    return inner
#登录

import datetime
import time
def login(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = Author.objects.filter(email=email,user_type=0).first()
            if user:
                ## 存在
                if user.password == setPassword(password):
                    ## 登录成功
                    ## 跳转页面
                    # error_msg = "登录成功"
                    # return HttpResponseRedirect('/index/')
                    ## 设置cookie
                    response  = HttpResponseRedirect("/Article/index/")
                    response.set_cookie("username",user.name)
                    response.set_cookie("userid",user.id)
                    request.session['username'] = user.name  ## 设置session
                    return response
                else:
                    error_msg = "密码错误"
            else:
                error_msg = "用户不存在"
        else:
            error_msg = "邮箱不可以为空"
    return render(request,"article/login.html",locals())

#首页
@LoginVaild
def index(request):
    # loginuser=LoginUser.objects.get(id=1)
    return render(request,'article/index.html')
    # return render(request, 'vuedemo.html')
#登出
def logout(request):
    #删除cookie 删除session
    respose=HttpResponseRedirect('/Article/login/')
    # respose.delete_cookie('kename')
    keys=request.COOKIES.keys()
    for one in keys:
        respose.delete_cookie(one)
    del request.session['username']
    return respose
#商品列表,分页：
def goods_list(request,status,page=1):

    """
    :param request:
    :param status: 想要获取的是 在售或者下架的商品 在售传参1 下架是0
    :param page:页
    :return:
    """
    #第一次
    page=int(page)
    # 第二次

    user_id = request.COOKIES.get("userid")
    print(user_id)
    # user = Author.objects.filter(id=user_id).first()
    user=Author.objects.get(id=user_id)
    print(user)
    #获取文章的作者：不行
    # writer = Article.objects.filter()
    #获取作者的文章

    if status == "0":
        # 下架商品
        goods_obj = user.article_set.filter(status=0).order_by("-id")
        # goods_obj = Article.objects.filter(status=0).order_by('id')
    else:
        # 在售商品
        goods_obj = user.article_set.filter(status=1).order_by("-id")
        # goods_obj = Article.objects.filter(status=1).order_by('id')

    # ar=user.article_set.all()
    # print(ar)
    # ar=user.Article_set.all()错

    # for one in ar:
    #     if one.status=="0":
    #         #下架商品
    #         goods_obj=ar.
    #         goods_obj=Article.objects.filter(status=0).order_by('id')
    #     else:
    #         #在售商品
    #         goods_obj=Article.objects.filter(status=1).order_by('id')


    # goods_obj=Goods.objects.all().order_by('goods_number')
    # print(goods_obj)
    goods_all=Paginator(goods_obj,10)
    goods_list=goods_all.page(page)
    # goods_list=Goods.objects.all()
    # 不需要返回数据，现在index就是访问的这一个
    # return render(request, "vue_goods_list.html")
    return render(request,'article/goods_list.html',locals())
## 商品状态
def goods_status(request,status,id):
#     """
#     完成当下架  修改status为0
#     当上架的 修改status为1
#status传过来的内容为up或者down
#     :param request:
#     :param status:操作内容  up 上架 down 下架
#     :param id: 商品id
#     :return:
#     """
    id=int(id)
    goods=Article.objects.get(id=id)
    if status=="up":
        #上架
        goods.status=1
    else:
        goods.status=0
    goods.save()
#当完成对这个对象的操作，修改状态，页面应该还是在当前页面不会改变
    # return  HttpResponseRedirect('/goods_list/1/1/')
    url=request.META.get("HTTP_REFERER","/Article/goods_list/1/1/")
    return HttpResponseRedirect(url)
#个人信息
@LoginVaild
def personal_info(request):
    user_id=request.COOKIES.get("userid")
    print(user_id)
    user=Author.objects.filter(id=user_id).first()
    if request.method=="POST":
        #获取 数据 ，保存数据
        data=request.POST
        print(data.get("email"))
        user.name=data.get("username")
        user.phone_number=data.get("phone_number")
        user.age=data.get("age")
        user.gender=data.get("gender")
        user.age=data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        print(request.FILES.get('photo'))
        user.photo = request.FILES.get("photo")
        user.save()
        print (data)
    return render(request,"article/personal_info.html",locals())

#卖家添加商品
@LoginVaild
def goods_add(request):
    ##处理post请求，获取数据，保存数据，返回响应
    goods_type=Type.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data)
        goods=Article()
        goods.title = data.get("title")
        goods.content = data.get("content")
        goods.description = data.get("description")
        goods.recommend = data.get("recommend")
        goods.click = data.get("click")
        goods.picture=request.FILES.get('picture')
        goods.status=1
        goods.save()
        #上面先获取到
        #下面添加类型外键
        #这是添加外键所在的列
        goods_type=request.POST.get("goods_type")#select标签的value类型是string
        print(goods_type)
        goods_type=[goods_type]
        #正向查询的两种方法
        #第一种方法，外键和上面的相等
        # goods.goods_type_id=int(goods_type)
        # goods.type=Type.objects.get(id=goods_type)#保存类型
        goods.type.set(goods_type)
        #保存店铺
        #从cookie中获取到用户信息
        user_id=request.COOKIES.get("userid")
        goods.author=Author.objects.get(id=user_id)
        goods.save()
    return  render(request,"article/goods_add.html",locals())





