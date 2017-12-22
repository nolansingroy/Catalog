from flask import Flask
app = Flask(__name__)


# Show all Organ Systems


@app.route('/')
@app.route('/RoadMapToHealth/')
def showOgranSystems():
    #restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    return "all organ systems are now visible"
    # return render_template('restaurants.html', restaurants=restaurants)

# Create a new restaurant


@app.route('/RoadMapToHealth/new/')  # methods=['GET','POST']
def newOrganSystem():
    return "create a new organ system, but really c'mon the human body only has 11!"
    '''
    #protecting the pages
    if  'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')
'''

# Edit a restaurant


@app.route('/RoadMapToHealth/organSystem_id/edit/')  # , methods=['GET', 'POST']
def editOrganSystem():  # organSystem_id
    return "Edit the specific organ system! "
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
    return "page to delete an organ system"

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
    return "displays all Organ Systems in the human body!"

    '''restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
       items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()
       return render_template('medicine.html', items=items, restaurant=restaurant)
    '''

# Create a new menu item


@app.route('/RoadMapToHealth/organSystem_id/medicine/new/')  # , methods=['GET', 'POST']
def newMedicine():  # organSystem_id
    return "page to create a new medicine"

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
    return "page to edit specific medicine"


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
    return "page to delete a specific medicine_id"
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
