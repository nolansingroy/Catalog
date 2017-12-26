from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Organ, Medicine

app = Flask(__name__)

##############################################################
# This is only for iterative step #3 Templates and Forms

# Adding Fake database using dictionary#################################
'''
# Fake Restaurants
organSystem = {'name': 'Digestive', 'id': '1'}

organSystems = [{'name': 'Digestive', 'id': '1'}, {
    'name': 'Heart', 'id': '2'}, {'name': 'Endocrine', 'id': '3'}]


# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
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
    # restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    # return "all organ systems are now visible"

# Create a new restaurant


@app.route('/RoadMapToHealth/new/')  # methods=['GET','POST']
def newOrganSystem():
    return render_template('newOrgan.html')

    '''
    # protecting the pages
    if  'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:'''

    # return "create a new organ system, but really c'mon the human body only has 11!"

# Edit a restaurant


@app.route('/RoadMapToHealth/organSystem_id/edit/')  # , methods=['GET', 'POST']
def editOrganSystem():  # organSystem_id
    return render_template('editOrgan.html', organSystem=organSystem)
    '''editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)
'''

# Delete a restaurant


@app.route('/RoadMapToHealth/organSystem_id/delete/')  # , methods=['GET', 'POST']
def deleteOrganSystem():  # OrganSystem_id
    return render_template('deleteOrgan.html', organSystem=organSystem)
    '''restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)
    '''
# Show a restaurant menu


@app.route('/RoadMapToHealth/organSystem_id/')
@app.route('/RoadMapToHealth/organSystem_id/medicine/')
def showMedicine():  # organSystem_id
    return render_template('medicine.html', items=items, organSystem=organSystem)

    '''restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
       items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()
       return render_template('medicine.html', items=items, restaurant=restaurant)
    '''

# Create a new menu item


@app.route('/RoadMapToHealth/organSystem_id/medicine/new/')  # , methods=['GET', 'POST']
def newMedicine():  # organSystem_id
    return render_template('newMedicine.html')

    '''restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
'''

# Edit a menu item


# , methods=['GET', 'POST']
@app.route('/RoadMapToHealth/organSystem_id/medicine/medicine_id/edit')
def editMedicine():  # organSystem_id,medicine_id
    return render_template('editMedicine.html', item=item)


'''
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
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
        return redirect(url_for('showMedicine', restaurant_id=restaurant_id))
    else:
        return render_template('editmedicine.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
'''

# Delete a menu item


# , methods=['GET', 'POST']
@app.route('/RoadMapToHealth/organSystem_id/medicine/medicine_id/delete')
def deleteMedicine():  # organSystem_id,medicine_id
    return render_template('deleteMedicine.html', item=item)
    #    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    #    if request.method == 'POST':
    #        session.delete(itemToDelete)
    #        session.commit()
    #        flash('Menu Item Successfully Deleted')
    #        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    #    else:
    #        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
