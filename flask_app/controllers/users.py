from flask import render_template, request, redirect, session, flash

from flask_app import app
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/users')


@app.route('/users')
def users():
    return render_template("users.html",users=User.get_all())


@app.route('/user/new')
def new():
    return render_template("new_user.html")

@app.route('/user/create',methods=['POST'])
def create():
    if User.is_valid_user(request.form):
        result = User.save(request.form)
        return redirect(f'/user/show/{result}')
    flash('regError')
    return redirect('/user/new')

@app.route('/user/edit/<int:id>')
def edit(id):
    return render_template("edit_user.html",user=User.get_one({"id": id}))

@app.route('/user/show/<int:id>')
def show(id):
    return render_template("show_user.html",user=User.get_one({"id": id}))

@app.route('/user/update',methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/users')

@app.route('/user/delete/<int:id>')
def delete(id):
    User.delete({'id': id})
    return redirect('/users')