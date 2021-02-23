from . import db
from .models import User
from .models import Steps
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route("/all")
@login_required
def user_stepsRecords():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    stepsRecords = user.stepsRecords  
    return render_template('stepsRecords.html', stepsRecords=stepsRecords, user=user)


@main.route("/new")
@login_required
def new_stepsRecord():
    return render_template('add_stepsRecord.html')


@main.route("/new", methods=['POST'])
@login_required
def add_new_stepsRecord():
    steps_completed = request.form.get('steps_completed')
    comment = request.form.get('comment')
    print(steps_completed, comment)
    stepsRecord = Steps(steps_completed=steps_completed, comment=comment, author=current_user)
    db.session.add(stepsRecord)
    db.session.commit()
    flash('Your steps details has been added!')
    return redirect(url_for('main.index'))


@main.route("/stepsRecord/<int:stepsRecord_id>/update", methods=['GET', 'POST'])
@login_required
def update_stepsRecord(stepsRecord_id):
    stepsRecord = Steps.query.get_or_404(stepsRecord_id)
    if request.method == "POST":        
        stepsRecord.steps_completed = request.form['steps_completed']
        stepsRecord.comment = request.form['comment']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.user_stepsRecords'))

    return render_template('update_stepsRecord.html', stepsRecord=stepsRecord)


@main.route("/stepsRecord/<int:stepsRecord_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_stepsRecord(stepsRecord_id):
    stepsRecord = Steps.query.get_or_404(stepsRecord_id)
    db.session.delete(stepsRecord)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('main.user_stepsRecords'))
