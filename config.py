import os
from datetime import timedelta
DEBUG=True
TEMPLATES_AUTO_RELOAD=True

USERNAME='root'
PASSWORD=''
HOST='127.0.0.1'
PORT='3306'
DATABASE='zlbbs'
DB_URI='mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(username=USERNAME,password=PASSWORD,host=HOST,port=PORT,db=DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False

SECRET_KEY=os.urandom(24)

PERMANENT_SESSION_LIFETIME=timedelta(days=15)

CMS_USER_ID='asda'
FRONT_USER_ID='Qwest'


# 发送者邮箱的服务器地址
MAIL_SERVER='smtp.qq.com'
MAIL_PORT='587'

# QQ邮箱不支持非加密的方式发送邮件
# port:587
MAIL_USE_TLS=True
# port:465

# MAIL_USE_SSL : default False

# MAIL_DEBUG : default app.debug

MAIL_USERNAME='1300067653@qq.com'
MAIL_PASSWORD='gbrmagsfffmuifgh'
MAIL_DEFAULT_SENDER='1300067653@qq.com'

# ALIDAYU_APP_KEY = 'LTAIXsMyFHp5Ro0L'
# ALIDAYU_APP_SECRET = 'DIqdvu7vfLIqB5E5cyUid3QuGTLErJ'
# ALIDAYU_SIGN_NAME = '来自韩丽君'
# ALIDAYU_TEMPLATE_CODE = 'SMS_126600242'

ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'


UEDITOR_UPLOAD_PATH=os.path.join(os.path.dirname(__file__),'images')

PER_PAGE=10

# celery相关的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"