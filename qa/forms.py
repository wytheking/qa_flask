import os.path

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from models import Question, db, QuestionTags, Answer


class WriteQuestionForm(FlaskForm):
    """ 写文章/问题 """
    img = FileField(label='上传图片', render_kw={
        'accept': ".jpeg, .jpg, .png",
    }, validators=[FileAllowed(['jpeg', 'jpg', 'png'], '暂不支持该图片类型')])
    title = StringField(label='标题', render_kw={
        'class': 'form-control',
        'placeholder': '请输入标题（长度为5-50字）',
        'required': False
    }, validators=[DataRequired('标题不能为空'),
                   Length(min=5, max=50, message='标题长度为5-50字')])
    tags = StringField(label='标签', render_kw={
        'class': 'form-control',
        'placeholder': '输入标签，用,分隔',
    })
    desc = TextAreaField(label='简述', render_kw={
        'class': 'form-control',
        'placeholder': '请输入简述（最多150字）',
    }, validators=[Length(max=150, message='简述最长150字')])
    content = CKEditorField(label='文章内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入正文',
        'required': False
    }, validators=[DataRequired('正文内容不能为空'), Length(min=5, message='正文内容不能少于5个字')])

    def save(self):
        """ 发布问题 """
        # 1、获取图片
        img = self.img.data
        if img:
            img_name = secure_filename(img.filename)
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2、保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        qa_obj = Question(img=img_name, title=title, desc=desc, content=content, user=current_user)
        db.session.add(qa_obj)
        # 3、保存标签
        tags = self.tags.data
        for tag_name in tags.split('，'):
            if tag_name:
                tag_obj = QuestionTags(tag_name=tag_name, question=qa_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return qa_obj


class WriteAnswerForm(FlaskForm):
    """ 写回答 """
    content = CKEditorField(label='回答内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入回答内容',
        'required': False
    }, validators=[DataRequired('回答内容不能为空'), Length(min=5, message='回答内容不能少于5个字')])

    def save(self, question):
        """ 提交答案 """
        content = self.content.data
        answer_obj = Answer(content=content, user=current_user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
