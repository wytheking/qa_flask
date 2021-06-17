import os.path


class Config(object):
    """ 项目的配置文件 """
    # 数据可链接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345678@127.0.0.1/flask_qa'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = '79537d00f4834892986f09a100aa1edf'
    WTF_CSRF_SECRET_KEY = 'f4834892986f09a100aa1edf'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'assets/medias/')
