from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,Resetpwd,ResetEmailForm,AddBanner,UpdateBanner,AddBoards,UpdateBoard
from .models import CMSUser,CMSPermission
from ..models import BannerModels,BoardModel,PostModel,HighLight
from .decorators import login_requried,permission_required
from exts import db,mail
from utils import restful,zlcache
from flask_mail import Message
import string,random
import config
from flask_wtf import CSRFProtect
from tasks import send_mail

bp=Blueprint('cms',__name__,url_prefix='/cms')


@bp.route('/')
@login_requried
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_requried
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/abanner/',methods=['POST'])
def abanner():
    form=AddBanner(request.form)
    if form.validate():
        name=form.name.data
        img_url=form.img_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=BannerModels(name=name,img_url=img_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramas_error(message=form.get_error())


@bp.route('/cms_banners/')
def banners():
    banners=BannerModels.query.order_by(BannerModels.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/ubanner/',methods=['POST'])
def ubanners():
    form=UpdateBanner(request.form)
    if form.validate():
        banner_id=form.banner_id.data
        name=form.name.data
        img_url=form.img_url.data
        link_url=form.link_url.data
        priority=form.priority.data
        banner=BannerModels.query.get(banner_id)
        if banner:
            banner.name=name
            banner.img_url=img_url
            banner.link_url=link_url
            banner.priority=priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramas_error(message='没有这个轮播图')
    else:
        return restful.paramas_error(message=form.get_error())


@bp.route('/dbanner/',methods=['POST'])
def dbanner():
    banner_id=request.form.get('banner_id')
    print(banner_id)
    if not banner_id:
        return restful.paramas_error(message='请传入轮播图参数')
    banner=BannerModels.query.get(banner_id)
    print(banner)
    if not banner:
        return restful.paramas_error(message='没有此数据')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()

@bp.route('/profile/')
@login_requried
@permission_required(CMSPermission.VISITOR)
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/boards/')
@login_requried
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models=BoardModel.query.all()
    context={
        'boards':board_models
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/aboards/',methods=['POST'])
@login_requried
@permission_required(CMSPermission.BOARDER)
def aboards():
    form=AddBoards(request.form)
    if form.validate():
        name=form.name.data
        board=BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramas_error(message='请选择版块')


@bp.route('/uboards/',methods=['POST'])
@login_requried
@permission_required(CMSPermission.BOARDER)
def uboards():
    form=UpdateBoard(request.form)
    if form.validate():
        board_id=form.board_id.data
        name=form.name.data
        board=BoardModel.query.get(board_id)
        if board:
            board.name=name
            db.session.commit()
            return restful.success()
        else:
            return restful.paramas_error(message='没有这个版块')
    else:
        return restful.paramas_error(message=form.get_error())


@bp.route('/dboards/',methods=['POST'])
@login_requried
@permission_required(CMSPermission.BOARDER)
def dboards():
    board_id=request.form.get('board_id')
    if not board_id:
        return restful.paramas_error(message='请传入版块ID')
    board=BoardModel.query.get(board_id)
    if board:
        db.session.delete(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramas_error(message='没有这个版块')


@bp.route('/comments/')
@login_requried
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/croles/')
@login_requried
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/cusers/')
@login_requried
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/fusers/')
@permission_required(CMSPermission.FRONTUSER)
@login_requried
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/posts/')
@login_requried
@permission_required(CMSPermission.POSTER)
def posts():
    context={
        'posts':PostModel.query.all()
    }
    return render_template('cms/cms_posts.html',**context)

@bp.route('/hpost/',methods=['POST'])
@login_requried
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id=request.form.get('post_id')
    if not post_id:
        return restful.paramas_error(message='请传入帖子ID')
    post=PostModel.query.get(post_id)
    if not post:
        return restful.paramas_error(message='没有这篇帖子')
    highlight=HighLight()
    highlight.post=post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()



@bp.route('/uhpost/',methods=['POST'])
@login_requried
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.paramas_error(message='请传入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramas_error(message='没有这篇帖子')
    print(post_id)
    highlight=HighLight.query.filter_by(post_id=post_id).first()
    print(highlight)
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/email_captcha/')
def email_captcha():
    email=request.args.get('email')
    if not email:
        restful.paramas_error('请输入正确的邮箱')
    source=list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(1,10)))
    captcha=''.join(random.sample(source,6))
    # message=Message('Python论坛邮箱验证码',recipients=[email],body='你的验证码是:%s'%captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.sever_error()
    send_mail.delay('小木虫论坛邮箱验证码',[email],'你的验证码是:%s'%captcha)
    zlcache.set(email,captcha)
    return restful.success()


class LoginView(views.MethodView):
    def get(self,error=None):
        return render_template('cms/cms_login.html',error=error)

    def post(self):
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            remember=form.remember.data
            user=CMSUser.query.filter_by(email=email).first()
            # print(user.username)
            if user and user.check_password(password):
                session[config.CMS_USER_ID]=user.id
                if remember:
                    session.permanent=True

                # print(session.get(config.CMS_USER_ID))
                return redirect(url_for('cms.index'))
            else:
                return self.get(error='邮箱或密码错误')
        else:

            return self.get(error=form.get_error())


class ResetView(views.MethodView):
    decorators = [login_requried]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form=Resetpwd(request.form)
        if form.validate() :
            oldpwd=form.oldpwd.data
            newpwd=form.newpwd.data
            user=g.cms_user
            if user.check_password(oldpwd):
                user.password=newpwd
                db.session.commit()
                # return jsonify({'code':200,'message':''})
                return restful.success()
            else:
                # return jsonify({'code':400,'message':'旧密码错误'})
                return restful.paramas_error('旧密码错误')
        else:
            return restful.paramas_error(form.get_error())

class ResetEmail(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form=ResetEmailForm(request.form)
        if form.validate():
            email=form.email.data
            g.cms_user.email=email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramas_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))