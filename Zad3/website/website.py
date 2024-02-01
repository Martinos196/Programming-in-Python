from flask import Blueprint, render_template, request, redirect, url_for, abort
from . import db


# sprawdza czy wartosc moze byc zmieniona na float
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


# definicja trasy dla głownej strony -> GET
@website.route('/', methods=['GET'])
def home():
    data = DataPoint.query.order_by(DataPoint.uid).all()
    return render_template("home.html", DataPoints=data)


# definicja trasy dla dodawania nowych danych - GET i POST
@website.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        if (is_float(request.form.get('feature1')) and is_float(request.form.get('feature2'))
                and request.form.get('category').isdigit()):
            new_data = DataPoint(feature1=float(request.form.get('feature1')),
                                 feature2=float(request.form.get('feature2')),
                                 category=request.form.get('category'))
            db.session.add(new_data)
            db.session.commit()
        else:
            abort(400)
        return redirect(url_for('website.home'))
    return render_template("add.html")


# def trasy dla usuwania danych na podstawie uid
@website.route('/delete/<int:uid>', methods=['GET', 'POST'])
def delete(uid):
    deleted_data = DataPoint.query.get(uid)
    if deleted_data:
        db.session.delete(deleted_data)
        db.session.commit()
    else:
        abort(404)
    return redirect(url_for('website.home'))
