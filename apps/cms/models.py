from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

cms_role_user=db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cmsrole.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cmsuser.id'),primary_key=True),
)

class CMSUser(db.Model):
    __tablename__='cmsuser'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(30),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(30),nullable=False,unique=True)
    join_time=db.Column(db.String(30),default=datetime.now)

    def __init__(self,username,password,email):
        self.username=username
        # 初始化时就会调用下面的property属性方法,采用加密的形式将密码添加到数据库表中
        self.password=password
        self.email=email


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password=generate_password_hash(raw_password)

    def check_password(self,raw_password):
        return check_password_hash(self.password,raw_password)

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions=0
        # 通过用户的roles属性拿到其权限
        for role in self.roles:
            permissions=role.permissions
            all_permissions |=permissions
        return all_permissions

    # 查看用户是否有某个权限,将这个用户的所有权限与这个权限做与运算,
    # 得到的结果与permission相等就说明有这个权限
    def has_permission(self,permission):
        # permissions也是CMSUser这个模型的属性
        all_permissions=self.permissions
        result=all_permissions&permission == permission
        return result

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)





class CMSPermission(object):
    ALL_PERMISSION=0b11111111#具有所有权限
    VISITOR=       0b00000001#访问权限
    POSTER=        0b00000010#管理帖子权限
    COMMENTER=     0b00000100#管理评论权限
    BOARDER=       0b00001000#管理板块权限
    FRONTUSER=     0b00010000#管理前台用户
    CMSUSER=       0b00100000#后台用户权限
    ADMINER=       0b01000000#管理后台用户

class CMSRole(db.Model):
    __tablename__='cmsrole'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time=db.Column(db.DateTime,default=datetime.now)
    permissions=db.Column(db.Integer,default=CMSPermission.VISITOR)

    users=db.relationship('CMSUser',secondary=cms_role_user,backref='roles')

