from django.http import HttpResponse
# return  HttpResponse('hello word')
from django.template import Template,Context
from django.shortcuts import render
from Article.models import *

from django.core.paginator import Paginator




def listpic(request):
    return render(request,'listpic.html')
def newslistpic(request,type,page=1):
    page=int(page)
    # article=Article.objects.order_by("-date")
    article=Type.objects.get(name=type).article_set.order_by("-date")
    paginator=Paginator(article,6)#每页显示6条数据
    page_obj=paginator.page(page)
    #获取当前页
    current_page=page_obj.number
    start=current_page-3
    if start<1:
        start=0
    end=current_page+2
    if end>paginator.num_pages:
        end=paginator.num_pages
    if start==0:
        end=5
    if end==paginator.num_pages:
        start=paginator.num_pages-5
    page_range=paginator.page_range[start:end]
    # print(article)
    return render(request,'newslistpic.html',locals())
def base(request):
    return render(request,'base.html')

def addarticle(request):
    for x in range(100):
        article=Article()
        article.title="title_%s"%x
        article.content="content_%s"%x
        article.description="description_%s"%x
        article.author=Author.objects.get(id=1)
        article.save()
        article.type.add(Type.objects.get(id=1))
        article.save()
    return HttpResponse('增加数据')
def articledetails(request,id):
    id=int(id)
    article=Article.objects.get(id=id)
    # print(article)
    paginator=Paginator(article,5)

    return render(request,'articledetails.html',locals())


def fytest(request):
    article=Article.objects.all().order_by("-date")
    print(article)
    return HttpResponse('分页测试')

def reqtest(request):
    #获取get请求传递的参数
    data=request.GET
    #获取post的请求参数
    # data=request.POST
    print(data)#<QueryDict: {'age': ['12'], 'name': ['zhnagsan']}>
    print(data.get("name"))
    print(type(data.get("name")))#<class 'str'>
    print(data.get("age"))
    return HttpResponse("姓名：%s年龄%s"%(data.get("name"),data.get("age")))


def formtest(request):
    #get请求
    data=request.GET
    # print(data)
    serach=data.get("serach")#文章标题
    print(serach)
    #通过form调教的数据，判断数据库中是否存在某个文章
    #通过模型进行查询
    #因为第一次访问只是出来页面，第二次才会get获得数据，第一次请求是空，空传递给filter，出现错误，
    # 所以需要,不为零的时候
    if serach:
        article=Article.objects.filter(title__contains=serach).all()
        print(article)
    return render(request,"formtest.html",locals())
def formtest2(request):
    print(request.method)
    data=request.POST
    print(data.get("username"))
    print(data.get('password'))
    return render(request,"formtest.html",locals())

import hashlib
def setPassword(password):
    #实现一个密码加密
    md5=hashlib.md5()#创建一个md5的一个实例对象
    md5.update(password.encode())#进行加密
    result=md5.hexdigest()#加密的结果
    return result

def register(request):
    if request.method=="POST":
        #获取用户数据
        username=request.POST.get("username")
        password=request.POST.get("password")
        password2=request.POST.get("password2")
        #判断是否有数据
        content='参数不全'
        if username and password2 and password:
            #判断密码是否相等
            if password!=password2:
                #return ""
                print("两次密码不一样")
                content="两次密码不一样"
            else:
                #保存数据
                user=User()
                user.name=username
                # user.password=password
                # 加密密码
                user.password = setPassword(password)
                user.save()
                content="添加成功"
    return render(request,"register.html",locals())
from Article.forms import Register
def register2(request):
    register2_form=Register()## 创建一个form表单类的实例对象
    if request.method=="POST":
        #获取用户数据
        # username=request.POST.get("username")
        username=request.POST.get("name")
        password=request.POST.get("password")
        # password2=request.POST.get("password2")
        #判断是否有数据
        content='参数不全'
        if username  and password:
            user=User()
            user.name=username
            #加密密码
            user.password=setPassword(password)
            user.save()
            content="添加成功"
    return render(request,"register2.html",locals())

from Article.forms import *
def register3(request):
    register3_form=Register()## 创建一个form表单类的实例对象
    if request.method=="POST":
        #获取用户数据
        # username=request.POST.get("username")
        username=request.POST.get("name")
        password=request.POST.get("password")
        print(username)
        # password2=request.POST.get("password2")
        #判断是否有数据
        content='参数不全'
        if username  and password:
            user=User()
            user.name=username
            #加密密码
            user.password=setPassword(password)
            user.save()
            content="添加数据成功"

    return render(request,"register3.html",locals())

def register4(request):
    register4_form=Register2()## 创建一个form表单类的实例对象
    error=''
    if request.method=="POST":
        #获取用户数据
        data=Register2(request.POST)#将post请求传递过来的数据，交给form表单类进行校验
        if data.is_valid():
            clean_data=data.cleaned_data
            #获取到数据，写库
            username=clean_data.get('name')
            password=clean_data.get('password')
            user=User()
            user.name=username
            #加密密码
            user.password=setPassword(password)
            user.save()
            error='添加数据成功'
        else:
            error=data.errors
            print(error)
    return render(request,'register3.html',locals())


def cspost(request):
    form_cspost=csforms()
    if request.method=='POST':
        clean_data=csforms(request.POST)
        if clean_data.is_valid():
            data=clean_data.cleaned_data
            username=data.get("username")
            content='成功'
        else:
            content=clean_data.errors
    return render(request,'csforms.html',locals())


from django.http import JsonResponse
def ajax_get(request):
    return render(request,'ajax_get.html')
def ajax_get_data(request):
    result={'code':10000,"content":""}
    data=request.GET
    username=data.get("username")
    password=data.get("password")
    if len(username)==0 or len(password)==0:
        result['code']=10001
        result['content']="请求参数为空"
    else:
        user=User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            result['code']=10000
            result['content']='用户可登录'
        else:
            result['code']=10002
            result['content']='用户不存在或者密码不正确'
    #返回一个json对象
    return JsonResponse(result)
    # return  HttpResponse("这个是ajax提交数据")

def ajax_post(request):
    return render(request,"ajax_post.html")
def ajax_post_data(request):
    #注册
    # result={"code":10000,"content":""}
    result={}
    username=request.POST.get('username')
    password=request.POST.get('password')
    if len(username)==0 or len(password)==0:
        result['code']=10001
        result["content"]='请求参数为空'
    else:
        #添加用户
        user=User()
        user.name=username
        user.password=setPassword(password)
        try:
            user.save()
            result['code']=10000
            result['content']='添加数据成功'
        except:
            result['code']=10002
            result['content']='添加数据错误'
    return JsonResponse(result)

def checkusername(request):
    result={"code":10001,"content":""}
    #get请求
    username=request.GET.get("name")
    print(username)
    #判断用户是否存在
    user=User.objects.filter(name=username).first()
    if user:
        #存在
        result={'code':10001,'content':'用户名已存在'}
    else:
        result={'code':10000,'content':'用户名不存在'}
    return  JsonResponse(result)
def index(request):
    #获取cookie 获取了用户名
    username=request.COOKIES.get("username")
    print(username)
    '''

   查询6条数据
   查询推荐的7条数据
   查询点击率排行榜的12条数据
    '''
    article=Article.objects.order_by("-date")[:6]
    recommend_article=Article.objects.order_by("-click")[:12]
    click_article=Article.objects.order_by("-click")[:12]
    # for i in article:
        # print(i.type)#Article.Type.None
        # print(i.type.first)
        # print(i.description)
    # print(article.date)
    return render(request,'index.html',locals())

## 登录装饰器
def loginVaild(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        username_session = request.session.get("username")

        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner
@loginVaild
def index2(request):


    #获取cookie 获取了用户名
    # username=request.COOKIES.get("username")
    # print("hha",username)
    # if username:
    print('lai')
    article = Article.objects.order_by("-date")[:6]
    recommend_article = Article.objects.order_by("-click")[:12]
    click_article = Article.objects.order_by("-click")[:12]
    return render(request, 'index.html', locals())

    # else:
    #     return HttpResponseRedirect('/login/')
@loginVaild
def about(request):
    return render(request,'about.html')

from django.http import  HttpResponseRedirect
def  login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #校验
        user=User.objects.filter(name=username).first()

        if user:
            #用户存在
            print('hiehi')

            if user.password==setPassword(password):
                print('enne')
                #密码正确
                #跳转页面 状态码 300 重定向
                # return HttpResponse('登录成功')
                #1.
                # return HttpResponseRedirect('/index/')
                #2.
                response=HttpResponseRedirect('/index2/')
                response.set_cookie('username','hello')

                request.session['username']=username

                return response

    return render(request,'login.html')

def logout(request):
    response=HttpResponseRedirect('/index2/')
    response.delete_cookie("username")
    #del request.session['username']
    request.session.flush()
    return response
