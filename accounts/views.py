from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import logout_user

from accounts.forms import RegisterForm, LoginForm

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='/assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录 """
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        next_url = request.values.get('next_url', url_for('qa.index'))
        user = form.do_login()
        if user:
            # 4、跳转到首页
            flash('{}， 欢迎回来!'.format(user.nickname), 'success')
            return redirect(next_url)
        else:
            flash('登录失败，请稍后再试!', 'danger')
    # else:
    #     print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout', methods=['GET', 'POST'])
def logout():
    """ 退出登录 """
    # 自定义登录情况下的退出登录逻辑代码
    # session['user_id'] = ''
    # g.current_user = None
    # flask-login 登录下的退出登录逻辑代码
    logout_user()
    flash('欢迎下次再来！', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册 """
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            # 3、跳转到成功页面
            flash('注册成功，请登录!', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('注册失败，请稍后再试!', 'danger')
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    """ 我的 """
    return render_template('mine.html')
