from django import  forms
class Register(forms.Form):
    name=forms.CharField(max_length=32)
    password=forms.CharField(max_length=32)


class Register2(forms.Form):
    name=forms.CharField(max_length=32)
    password=forms.CharField(max_length=32)
    #固定写法
    def clean_name(self):
        '''
        自定义校验  用户名不允许是admin
        '''
        name=self.cleaned_data.get('name')
        if name=='admin':
            self.add_error('name','不可以是admin')
        else:
            return name
class csforms(forms.Form):
    username=forms.CharField(max_length=8,min_length=6,label='姓名')
    def clean_username(self):
        username=self.cleaned_data.get('username')
        #判断 username中是否包含特殊字符 比如G adminnG
        if 'G' in username:
            self.add_error('username','不可以是%s'%username)
        else:
            return username
