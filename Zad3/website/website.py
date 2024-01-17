from flask import abort, Blueprint, redirect, render_template, request, url_for
from . import db
import uuid


class DataClass(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    feature1 = db.Column(db.Float)
    feature2 = db.Column(db.Float)
    category = db.Column(db.Integer)


website = Blueprint('website', __name__)


@website.route('/', methods=['GET', 'POST'])
def home():
    data = DataClass.query.order_by(DataClass.category).all()
    if request.method == 'POST':
        uid = request.form.get("uid")
        return redirect(url_for('website.delete', uid=uid))
    return render_template("home.html", DataClass=data)


@website.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        uid = str(uuid.uuid4().int)[:10]
        try:
            if (request.form.get('feature1').isdigit() and request.form.get('feature2').isdigit()
                    and request.form.get('category').isdigit()):
                new_data = DataClass(uid=uid, feature1=request.form.get('feature1'),
                                     feature2=request.form.get('feature2'), category=request.form.get('category'))
                db.session.add(new_data)
                db.session.commit()
            else:
                raise ValueError("Wrong data")
        except Exception as e:
            print(e)
            return abort(400)
        return redirect(url_for('website.home'))
    return render_template("add.html")


@website.route('/delete/<int:uid>', methods=['GET', 'POST'])
def delete(uid):
    try:
        deleted_data = DataClass.query.get(uid)
        if deleted_data:
            db.session.delete(deleted_data)
            db.session.commit()
        else:
            raise ValueError("Record not found")
    except Exception as e:
        print(e)
        return abort(404)
    return redirect(url_for('website.home'))
