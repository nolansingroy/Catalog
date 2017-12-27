from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Organ, Medicine

app = Flask(__name__)

##############################################################
# This is only for iterative step #3 Templates and Forms

# Adding Fake database using dictionary#################################
'''
# Fake organs
organSystem = {'name': 'Digestive', 'id': '1'}

organSystems = [{'name': 'Digestive', 'id': '1'}, {
    'name': 'Heart', 'id': '2'}, {'name': 'Endocrine', 'id': '3'}]


# Fake organs
organ = {'name': 'The CRUDdy Crab', 'id': '1'}

organs = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
    'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]
# Fake Menu Items
items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables',
                                                                                                                                                                                                                                                        'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]

item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
        'price': '$5.99', 'course': 'Entree'}
'''

###########################################################################
# Add our Database


engine = create_engine('sqlite:///roadmaptohealth.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#########################################################################
# Show all Organ Systems


@app.route('/')
@app.route('/RoadMapToHealth/')
def showOrganSystems():
    organ = session.query(Organ).all()
    return render_template('organSystems.html', organ=organ)
    # organs = session.query(organ).order_by(asc(organ.name))
    # return "all organ systems are now visible"

# Create a new organ


@app.route('/RoadMapToHealth/new/', methods=['GET', 'POST'])
def newOrganSystem():
    # protecting the pages
    # if  'username' not in login_session:
    #    return redirect('/login')
    if request.method == 'POST':
        newOrgan = Organ(name=request.form['name'])
        session.add(newOrgan)
        #flash('New organ %s Successfully Created' % neworgan.name)
        session.commit()
        return redirect(url_for('showOrganSystems'))
    else:
        return render_template('newOrgan.html')
# Edit a organ


@app.route('/RoadMapToHealth/<int:organ_id>/edit/', methods=['GET', 'POST'])
def editOrganSystem(organ_id):  # organSystem_id
    # return render_template('editOrgan.html', organSystem=organSystem)
    editedOrgan = session.query(
        Organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedOrgan.name = request.form['name']
            #flash('Organ Successfully Edited %s' % editedOrgan.name)
            return redirect(url_for('showOrganSystems'))
    else:
        return render_template('editOrgan.html', organ=editedOrgan, organ_id=organ_id)


# Delete a organ


@app.route('/RoadMapToHealth/<int:organ_id>/delete/', methods=['GET', 'POST'])
def deleteOrganSystem(organ_id):  # OrganSystem_id
    # return render_template('deleteOrgan.html', organSystem=organSystem)
    organToDelete = session.query(
        Organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        session.delete(organToDelete)
        #flash('%s Successfully Deleted' % organToDelete.name)
        session.commit()
        return redirect(url_for('showOrganSystems', organ_id=organ_id))
    else:
        return render_template('deleteOrgan.html', organ=organToDelete)

# Show a organ menu


@app.route('/RoadMapToHealth/<int:organ_id>/')
@app.route('/RoadMapToHealth/<int:organ_id>/medicine/')
def showMedicine(organ_id):  # organSystem_id
    # return render_template('medicine.html', items=items, organSystem=organSystem)
    organ = session.query(Organ).filter_by(id=organ_id).one()
    items = session.query(Medicine).filter_by(organ_id=organ_id).all()
    return render_template('medicine.html', items=items, organ=organ)


# Create a new menu item


@app.route('/RoadMapToHealth/<int:organ_id>/medicine/new/', methods=['GET', 'POST'])
def newMedicine(organ_id):
    # return render_template('newMedicine.html')
    organ = session.query(Organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        newItem = Medicine(name=request.form['name'], description=request.form[
                           'description'], type=request.form['type'], gland=request.form['gland'], organ_id=organ_id, organ=organ)
        session.add(newItem)
        session.commit()
        #flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('newMedicine.html', organ_id=organ_id)


# Edit a menu item

@app.route('/RoadMapToHealth/<int:organ_id>/medicine/<int:medicine_id>/edit', methods=['GET', 'POST'])
def editMedicine(organ_id, medicine_id):  # organSystem_id,medicine_id
    # return render_template('editMedicine.html', item=item)
    editedItem = session.query(Medicine).filter_by(id=medicine_id).one()
    organ = session.query(Organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['gland']:
            editedItem.price = request.form['gland']
        if request.form['type']:
            editedItem.course = request.form['type']
        session.add(editedItem)
        session.commit()
        #flash('Menu Item Successfully Edited')
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('editMedicine.html', organ_id=organ_id, medicine_id=medicine_id, item=editedItem)


# Delete a menu item


@app.route('/RoadMapToHealth/<int:organ_id>/medicine/<int:medicine_id>/delete', methods=['GET', 'POST'])
def deleteMedicine(organ_id, medicine_id):  # organSystem_id,medicine_id
    # return render_template('deleteMedicine.html', item=item)
    organ = session.query(Organ).filter_by(id=organ_id).one()
    itemToDelete = session.query(Medicine).filter_by(id=medicine_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
    #        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('deleteMedicine.html', item=itemToDelete, organ_id=organ_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
