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


@app.route('/RoadMapToHealth/organSystem_id/')
@app.route('/RoadMapToHealth/organSystem_id/medicine/')
def showMedicine():  # organSystem_id
    return render_template('medicine.html', items=items, organSystem=organSystem)

    '''organ = session.query(organ).filter_by(id=organ_id).one()
       items = session.query(MenuItem).filter_by(
            organ_id=organ_id).all()
       return render_template('medicine.html', items=items, organ=organ)
    '''

# Create a new menu item


@app.route('/RoadMapToHealth/organSystem_id/medicine/new/')  # , methods=['GET', 'POST']
def newMedicine():  # organSystem_id
    return render_template('newMedicine.html')

    '''organ = session.query(organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], organ_id=organ_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', organ_id=organ_id))
    else:
        return render_template('newmenuitem.html', organ_id=organ_id)
'''

# Edit a menu item


# , methods=['GET', 'POST']
@app.route('/RoadMapToHealth/organSystem_id/medicine/medicine_id/edit')
def editMedicine():  # organSystem_id,medicine_id
    return render_template('editMedicine.html', item=item)


'''
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    organ = session.query(organ).filter_by(id=organ_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMedicine', organ_id=organ_id))
    else:
        return render_template('editmedicine.html', organ_id=organ_id, menu_id=menu_id, item=editedItem)
'''

# Delete a menu item


# , methods=['GET', 'POST']
@app.route('/RoadMapToHealth/organSystem_id/medicine/medicine_id/delete')
def deleteMedicine():  # organSystem_id,medicine_id
    return render_template('deleteMedicine.html', item=item)
    #    organ = session.query(organ).filter_by(id=organ_id).one()
    #    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    #    if request.method == 'POST':
    #        session.delete(itemToDelete)
    #        session.commit()
    #        flash('Menu Item Successfully Deleted')
    #        return redirect(url_for('showMenu', organ_id=organ_id))
    #    else:
    #        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
