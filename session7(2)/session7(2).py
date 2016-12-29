from flask import Flask, redirect, url_for, render_template, request, flash, session
import mongoengine
from mongoengine import *

host = "ds139278.mlab.com"
port = 39278
db_name = "trangdatabase"
user_name = "DoTrang"
password = "12345678"

mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)
app = Flask(__name__)
app.secret_key = "super secret key"


class place(Document):
      name = StringField()
      picture = URLField()
      WebLink = URLField()


@app.route('/')
def openMyBlog():
    return render_template('MyBlog.html', Place_list = place.objects)


@app.route('/Info')
def openInfosite():
    return render_template('Info-site.html')

@app.route("/add_place", methods=["GET","POST"])
def add_place():
    if request.method == "GET":
        return render_template("add_place.html")
    elif request.method == "POST":
        name =request.form["Your place is"]
        picture=request.form["Give a picture"]
        WebLink = request.form["Link to a web page"]
        # object
        placeAdded = place(name = name, picture = picture, WebLink = WebLink) #Constructor
        placeAdded.save()
        flash('Thanks for your supporting')
        return redirect(url_for('openMyBlog'))


@app.route("/delete_place/<place_id>")
def delete_place(place_id):
    placeDeleted = place.objects.with_id(place_id)
    placeDeleted.delete()
    flash('The place is deleted!')
    return redirect(url_for('openMyBlog'))

@app.route("/update_place/<place_id>", methods=["GET","POST"])
def update_place(place_id):
    placeUpdated= place.objects.with_id(place_id)
    if request.method == "GET":
        return render_template("update_place.html",place = placeUpdated)
    elif request.method == "POST":
        Newname =request.form["name"]
        Newpicture = request.form["picture"]
        Newlink = request.form["WebLink"]
        placeUpdated.update(set__name = Newname, set__picture= Newpicture, set__WebLink= Newlink)
        return redirect(url_for('openMyBlog'))





if __name__ == '__main__':
    app.run()