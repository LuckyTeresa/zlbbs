from .views import bp
import config
from flask import session,g,render_template
from .models import FrontUser

# hooks在这个单独的文件中没有与cms中的函数产生关联,将其导入__init__中

# 在钩子函数中将用户信息绑定到g对象上,然后再访问主页时就可以在主页的模板中使用这个g对象
@bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        user_id=session.get(config.FRONT_USER_ID)
        user=FrontUser.query.get(user_id)
        if user:
            g.front_user=user


@bp.errorhandler
def page_not_found():
    return render_template('front/front_404.html'),404