from flask import Blueprint,request,make_response
from exts import alidayu
from utils import restful,zlcache
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO#专门用于写二进制流数据
from tasks import send_sms_captcha


bp=Blueprint('commom',__name__,url_prefix='/c')

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone=request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码')
#     captcha=Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         return restful.params_error(message='短信验证码发送失败')


@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
#     telephone+timestamp+salt
    form=SMSCaptchaForm(request.form)
    if form.validate():
        telephone=form.telephone.data
        captcha=Captcha.gene_text(number=4)
        print('生成的短信验证码:%s'%captcha)
        # if alidayu.send_sms(telephone,code=captcha):
        #     zlcache.set(telephone,captcha)
        #     return restful.success()
        # else:
        #     # return restful.paramas_error(message='参数错误')
        #     zlcache.set(telephone,captcha)
        send_sms_captcha.delay(telephone,captcha)
        return restful.success()
    else:
        return restful.paramas_error(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text,image=Captcha.gene_graph_captcha()
    print('图形验证码:%s'%text)
    zlcache.set(text.lower(),text.lower())
    # BytesIO:字节流  创建二进制流对象
    out=BytesIO()
    image.save(out,'png')
    # 将文件指针放到最开始位置,方便下面读取.如果指针在最末尾,读取不到文件
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type='image/png'
    # resp.content_type='application/octet-stream'
    return resp




