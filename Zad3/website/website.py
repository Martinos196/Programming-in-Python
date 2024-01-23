from flask import Blueprint, render_template, request, redirect, url_for, abort
from . import db
import uuid

#sprawdza czy wartosc moze byc zmieniona na float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class DataPoint(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    feature1 = db.Column(db.Float)
    feature2 = db.Column(db.Float)
    category = db.Column(db.Integer)

website = Blueprint('website', __name__)

#definicja trasy dla głownej strony -> GET i POST
@website.route('/', methods=['GET', 'POST'])
def home():
    data = DataPoint.query.order_by(DataPoint.category).all()
    if request.method == 'POST':
        uid = request.form.get("uid")
        return redirect(url_for('website.delete', uid=uid))
    return render_template("home.html", DataPoints=data)

#definicja trasy dla dodawania nowych danych - GET i POST
@website.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        uid = str(uuid.uuid4().int)[:10]
        try:
            if (is_float(request.form.get('feature1')) and is_float(request.form.get('feature2'))
                    and request.form.get('category').isdigit()):
                new_data = DataPoint(uid=uid, feature1=float(request.form.get('feature1')),
                                     feature2=float(request.form.get('feature2')), category=request.form.get('category'))
                db.session.add(new_data)
                db.session.commit()
            else:
                raise ValueError("Wrong data")
        except Exception as e:
            print(e)
            return abort(400)
        return redirect(url_for('website.home'))
    return render_template("add.html")

#def trasy dla usuwania danych na podstawie uid
@website.route('/delete/<int:uid>', methods=['GET', 'POST'])
def delete(uid):
    try:
        deleted_data = DataPoint.query.get(uid)
        if deleted_data:
            db.session.delete(deleted_data)
            db.session.commit()
        else:
            raise ValueError("Not found")
    except Exception as e:
        print(e)
        return abort(404)
    return redirect(url_for('website.home'))
