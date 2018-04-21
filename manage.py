from flask_script import Manager
from zlbbs import app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModels,BoardModel,PostModel,HighLight

CMSUser=cms_models.CMSUser
CMSRole=cms_models.CMSRole
CMSPermission=cms_models.CMSPermission

FrontUser=front_models.FrontUser


manager=Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


# 在终端执行的时候  python manager.py create_cms_user -u han -p 123 -e 12345@qq.com
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user=CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

@manager.command
def create_role():
    # 创建role
    visitor=CMSRole(name='访问者',desc='只能访问想关数据,不能修改')
    visitor.permissions=CMSPermission.VISITOR

    operator=CMSRole(name='运营',desc='管理帖子,管理评论,管理前台用户')
    operator.permissions=CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER |CMSPermission.CMSUSER| CMSPermission.FRONTUSER

    # 管理员:拥有绝大部分权限
    admin=CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions=CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER |CMSPermission.CMSUSER| CMSPermission.FRONTUSER|CMSPermission.BOARDER

    developer=CMSRole(name='开发者',desc='开发人员专用')
    developer.permissions=CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user=CMSUser.query.filter_by(email=email).first()
    if user:
        role=CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('角色添加成功')
        else:
            print('此角色不存在')
    else:
        print('此邮箱用户不存在')




@manager.command
def test_permission():
    user=CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('这个用户有访问者权限')
    else:
        print('这个用户没有访问者权限')


@manager.command
def is_developer():
    user=CMSUser.query.filter_by(id=5).first()
    if user.is_developer:
        print('这个用户有开发者权限')
    else:
        print('这个用户没有开发者权限')

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user=FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_test_post():
    for x in range(1,205):
        title='我是标题%s'%x
        content='我是内容,我的编号是%s'%x
        board=BoardModel.query.first()
        author=FrontUser.query.first()
        post=PostModel(title=title,content=content)
        post.board=board
        post.author=author
        db.session.add(post)
        db.session.commit()
    print('测试帖添加成功')


if __name__ == '__main__':
    manager.run()


