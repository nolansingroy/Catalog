#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Organ, Medicine, User

# IMPORTS FOR GOOGLE credentials

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, flash, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web'
                                                               ]['client_id']
APPLICATION_NAME = 'RoadMapToHealth'

#########################################################################
# Add our Database

engine = create_engine('sqlite:///roadmaptohealthwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#########################################################################

# Create anti-forgery state token

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    # return "The current session state is %s" % login_session['state']

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'
                                            ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("Token's client ID does not match app's."
                                     ), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                                     ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# see if user exists, if not then make new user

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """
              " style = "width: 300px; height: 300px;border-radius: 150px;
              -webkit-border-radius: 150px;-moz-border-radius: 150px;">
              """
    flash('you are now logged in as %s' % login_session['username'])
    print 'done!'
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'
                                            ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response


#####################################################################
# JSON API's

# /RoadMapToHealth/JSON

@app.route('/RoadMapToHealth/JSON')
def organSystemsJSON():
    organSystems = session.query(Organ).all()
    return jsonify(organSystems=[o.serialize for o in organSystems])


# /RoadMapToHealth/organ_id/medicine/JSON

@app.route('/RoadMapToHealth/<int:organ_id>/medicine/JSON')
def organSystemsMedicineJSON(organ_id):
    organSystems = session.query(Organ).filter_by(id=organ_id).one()
    items = session.query(Medicine).filter_by(organ_id=organ_id).all()
    return jsonify(MedicineItems=[i.serialize for i in items])


# /RoadMapToHealth/organ_id/medicine/medicine_id/JSON

@app.route('/RoadMapToHealth/<int:organ_id>/medicine/<int:medicine_id>/JSON'
           )
def medicineItemJSON(organ_id, medicine_id):
    Medicine_Item = \
        session.query(Medicine).filter_by(id=medicine_id).one()
    return jsonify(Medicine_Item=Medicine_Item.serialize)


######################################################################

# Show information of a specific item

@app.route('/RoadMapToHealth/<path:organ_name>/<path:medicine_name>')
def showSpecificMedicine(organ_name, medicine_name):
    organ = session.query(Organ).filter_by(name=organ_name).one()
    item = session.query(Medicine).filter_by(name=medicine_name,
                                             organ=organ).one()
    return render_template('showSpecificMedicine.html', item=item, organ=organ)
#######################################################################
# Show all Organ Systems


@app.route('/')
@app.route('/RoadMapToHealth/')
def showOrganSystems():
    organ = session.query(Organ).order_by(asc(Organ.name))
    items = \
        session.query(Medicine).order_by(desc(Medicine.time_created))
    if 'username' not in login_session:
        return render_template(
            'publicOrganSystems.html',
            organ=organ,
            items=items)
    else:
        return render_template('organSystems.html', organ=organ,
                               items=items)


# Create a new organ

@app.route('/RoadMapToHealth/new/', methods=['GET', 'POST'])
def newOrganSystem():

    # protecting the pages

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newOrgan = Organ(name=request.form['name'],
                         user_id=login_session['user_id'])
        session.add(newOrgan)
        flash('New organ %s Successfully Created' % newOrgan.name)
        session.commit()
        return redirect(url_for('showOrganSystems'))
    else:
        return render_template('newOrgan.html')


# Edit a organ

@app.route('/RoadMapToHealth/<int:organ_id>/edit/', methods=['GET',
                                                             'POST'])
def editOrganSystem(organ_id):

    # page protection

    if 'username' not in login_session:
        return redirect('/login')
    editedOrgan = session.query(Organ).filter_by(id=organ_id).one()
    if editedOrgan.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized" \
            "to edit this organ.Please create your own in order" \
            "to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedOrgan.name = request.form['name']
            flash('Organ %s successfully edited ' % editedOrgan.name)
            return redirect(url_for('showOrganSystems'))
    else:
        return render_template('editOrgan.html', organ=editedOrgan,
                               organ_id=organ_id)


# Delete a organ

@app.route('/RoadMapToHealth/<int:organ_id>/delete/', methods=['GET',
                                                               'POST'])
def deleteOrganSystem(organ_id):

    # protecting the page

    if 'username' not in login_session:
        return redirect('/login')
    organToDelete = session.query(Organ).filter_by(id=organ_id).one()
    if organToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized" \
            "to delete this organ.Please create your own in order"\
            "to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(organToDelete)
        flash('%s Successfully Deleted' % organToDelete.name)
        session.commit()
        return redirect(url_for('showOrganSystems', organ_id=organ_id))
    else:
        return render_template('deleteOrgan.html', organ=organToDelete)


# Show a organ menu

@app.route('/RoadMapToHealth/<int:organ_id>/')
@app.route('/RoadMapToHealth/<int:organ_id>/medicine/')
def showMedicine(organ_id):
    organ = session.query(Organ).filter_by(id=organ_id).one()
    items = session.query(Medicine).filter_by(organ_id=organ_id).all()
    creator = getUserInfo(organ.user_id)
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return render_template('publicMedicine.html', items=items,
                               organ=organ, creator=creator)
    else:
        return render_template('medicine.html', items=items,
                               organ=organ, creator=creator)


#######################################################################
# Header Render Template Routes

@app.route('/RoadMapToHealth/Ayurvedic')
def ayurvedic():
    return render_template('ayurvedic.html')


@app.route('/RoadMapToHealth/Peptide')
def peptide():
    return render_template('peptide.html')


@app.route('/RoadMapToHealth/Supplement')
def supplement():
    return render_template('supplement.html')


@app.route('/RoadMapToHealth/Hormone')
def hormone():
    return render_template('hormone.html')


@app.route('/RoadMapToHealth/TCM')
def tcm():
    return render_template('tcm.html')


@app.route('/RoadMapToHealth/Contact')
def contact():
    return render_template('contact.html')


# Create a new menu item

@app.route('/RoadMapToHealth/<int:organ_id>/medicine/new/',
           methods=['GET', 'POST'])
def newMedicine(organ_id):

    # Page Protection

    if 'username' not in login_session:
        return redirect('/login')
    organ = session.query(Organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        newItem = Medicine(
            name=request.form['name'],
            description=request.form['description'],
            type=request.form['type'],
            gland=request.form['gland'],
            organ_id=organ_id,
            organ=organ,
            user_id=organ.user_id
        )
        session.add(newItem)
        session.commit()
        flash('New Medicine %s Successfully Created' % newItem.name)
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('newMedicine.html', organ_id=organ_id)


# Edit a menu item

@app.route(
    '/RoadMapToHealth/<int:organ_id>/medicine/<int:medicine_id>/edit',
    methods=[
        'GET',
        'POST'])
def editMedicine(organ_id, medicine_id):

    # Page Protection

    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Medicine).filter_by(id=medicine_id).one()
    organ = session.query(Organ).filter_by(id=organ_id).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized" \
            "to edit this organ.Please create your own in order"\
            "to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['gland']:
            editedItem.gland = request.form['gland']
        if request.form['type']:
            editedItem.type = request.form['type']
        session.add(editedItem)
        session.commit()
        flash('Medicine %s Successfully Edited' % editedItem.name)
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('editMedicine.html', organ_id=organ_id,
                               medicine_id=medicine_id, item=editedItem)


# Delete a menu item

@app.route(
    '/RoadMapToHealth/<int:organ_id>/medicine/<int:medicine_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteMedicine(organ_id, medicine_id):

    # page Protection

    if 'username' not in login_session:
        return redirect('/login')
    organ = session.query(Organ).filter_by(id=organ_id).one()
    itemToDelete = \
        session.query(Medicine).filter_by(id=medicine_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('you are not authorized" \
            "to delete this organ.Please create your own in order"\
            "to delete.');}</script><body onload='myFunction()'>'"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Medicine Successfully Deleted')
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('deleteMedicine.html',
                               item=itemToDelete, organ_id=organ_id)


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email'
                                                             ]).one()
    return user.id


#if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
#    app.run(host='0.0.0.0', port=8000)
