# 在Python包中导入同级文件,前面加 .  ,主目录下不需要
from .views import bp
# python3中直接使用import语句,就要从主目录开始导入,主目录下不需要
import apps.cms.hooks