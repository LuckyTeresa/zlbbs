from flask import Blueprint, views, render_template, Response, make_response, jsonify, request, session, url_for, g,abort
from utils.captcha import Captcha
from .forms import SignupForm, SigninForm, AddPost,AddComment
from exts import alidayu
from utils import restful, safeutils
from .models import FrontUser
from ..models import BannerModels, BoardModel, PostModel,CommentOmdel,HighLight
from exts import db
from .decorators import login_requried
import config
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.sql import func
bp = Blueprint('front', __name__)


# @bp.route('/sms_captcha/')
# def sms_captcha():
#     result=alidayu.send_sms('13554541538',code='aswe')
#     if result:
#         return 'success'
#     else:
#         return 'faild'

@bp.route('/')
def index():
    board_id=request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort=request.args.get('st',type=int,default=1)

    banners = BannerModels.query.order_by(BannerModels.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts=None
    total=0
    query_obj=None
    if sort==1:
        query_obj=PostModel.query.order_by(PostModel.create_time.desc())
    elif sort==2:
        query_obj=db.session.query(PostModel).outerjoin(HighLight).order_by(HighLight.create_time.desc(),PostModel.create_time.desc())
    elif sort==3:
        query_obj=PostModel.query.order_by(PostModel.create_time.desc())
    elif sort==4:
        query_obj=db.session.query(PostModel).outerjoin(CommentOmdel).group_by(PostModel.id).order_by(func.count(CommentOmdel.id).desc(),PostModel.create_time.desc())

    if board_id:
        query_obj=query_obj.filter(PostModel.board_id==board_id)
        posts=query_obj.slice(start, end)
        total=query_obj.count()
    else:
        posts = query_obj.slice(start, end)
        total = query_obj.count()

    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board':board_id,
        'current_sort':sort
    }
    return render_template('front/front_index.html', **context)

@bp.route('/p/<post_id>')
def post_detail(post_id):
    print(post_id)
    post=PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_postdetail.html',post=post)


@bp.route('/apost/', methods=['POST', 'GET'])
@login_requried
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        form = AddPost(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.paramas_error(message='没有这个版块')
            post = PostModel(title=title, content=content, board_id=board_id)
            post.author = g.front_user
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramas_error(message=form.get_error())

@bp.route('/acomment/',methods=['POST'])
@login_requried
def add_comment():
    form=AddComment(request.form)
    if form.validate():
        content=form.content.data
        post_id=form.post_id.data
        post=PostModel.query.get(post_id)
        if post:
            comment=CommentOmdel(content=content)
            comment.post=post
            comment.author=g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramas_error(message='没有这个帖子')
    else:
        return restful.paramas_error(form.get_error())


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.paramas_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(
                return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.paramas_error(message='手机号或密码错误')
        else:
            return restful.paramas_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
