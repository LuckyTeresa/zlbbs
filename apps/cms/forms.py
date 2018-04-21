from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email=StringField(validators=[Email(message='请输入正确的邮箱'),InputRequired(message='请输入邮箱')])
    password=StringField(validators=[Length(3,10,message='请输入正确格式的密码'),InputRequired(message='请输入邮箱')])
    remember=IntegerField()

class Resetpwd(BaseForm):
    oldpwd=StringField(validators=[Length(3,10,message='请输入正确格式的密码')])
    newpwd=StringField(validators=[Length(3,10,message='请输入正确格式的密码')])
    newpwd2=StringField(validators=[EqualTo('newpwd',message='与上次输入不一致')])

class ResetEmailForm(BaseForm):
    email=StringField(validators=[Email(message='请输入正确的邮箱'),InputRequired(message='请输入邮箱')])
    captcha=StringField(validators=[Length(min=6,max=6,message='验证码长度为6位')])

    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        captcha_cache=zlcache.get(email)
        if not captcha_cache or captcha_cache.lower() !=captcha.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self,field):
        email=field.data
        user=g.cms_user
        if user.email==email:
            raise ValidationError('不能修改为原邮箱')


class AddBanner(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入图片名称')])
    img_url=StringField(validators=[InputRequired(message='请输入图片链接')])
    link_url=StringField(validators=[InputRequired(message='请输入跳转链接')])
    priority=IntegerField(validators=[InputRequired(message='请输入优先级')])


class UpdateBanner(AddBanner):
    banner_id=IntegerField(validators=[InputRequired(message='请输入轮播图ID')])

class AddBoards(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入版块名称'),Length(2,15,message='长度应在2-15个字符之间')])

class UpdateBoard(AddBoards):
    board_id=IntegerField(validators=[InputRequired(message='请输入版块名称')])

