from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
GENDER_LIST=(
    (1,'男'),
    (2,'女'),
)
class Author(models.Model):
    name=models.CharField(max_length=32,verbose_name="作者名字")
    age=models.IntegerField(verbose_name="年龄",null=True,blank=True)
    # gender=models.CharField(max_length=8,verbose_name="性别")
    gender=models.IntegerField(choices=GENDER_LIST,verbose_name="性别",default=1)
    email=models.CharField(max_length=32,verbose_name="邮箱")

    password = models.CharField(max_length=32,null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    photo = models.ImageField(upload_to="images", null=True, blank=True)  # 目录：static/images
    address = models.TextField(null=True, blank=True)
    # 0代表的作家  1代表读者  2管理员
    user_type = models.IntegerField(default=1)
    def __str__(self):
        return  self.name
    class Meta:
        db_table='author'
        verbose_name='作者'
        verbose_name_plural=verbose_name

class Type(models.Model):
    name=models.CharField(max_length=32,verbose_name="类型名字")
    description=models.TextField(verbose_name="类型描述")
    def __str__(self):
        return  self.name
    class Meta:
        db_table='type'
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title=models.CharField(max_length=32,verbose_name="文章")
    date=models.DateField(auto_now=True,verbose_name="日期")
    # content=models.TextField(verbose_name="文章内容")
    content=RichTextField()
    # description=models.TextField(verbose_name="文章描述")
    description=RichTextField()
    # 图片类型
    # upload_to 指定文件上传位置 static 目录下的 images目录中
    picture = models.ImageField(upload_to='images')
    recommend=models.IntegerField(verbose_name="推荐",default=0)
    click=models.IntegerField(verbose_name="点击率",default=0)
    status=models.IntegerField(default=1)#0代表下架，1代表上架
    author=models.ForeignKey(to=Author,on_delete=models.SET_DEFAULT,default=1)#一个作者多篇文章
    type=models.ManyToManyField(to=Type)#一个类型很多篇文章,一篇文章有多个类型

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class User(models.Model):
    name=models.CharField(max_length=32)
    password=models.CharField(max_length=32)

    class Meta:
        db_table="user"