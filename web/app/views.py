from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user


from app import app
from app import db
from app import login_manager


from app.models.contact import Contact
from app.models.authuser import AuthUser, PrivateContact

# import json
# from app.models.blogentry import BlogEntry


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))


@app.route('/')
def home():
    return "Flask says 'Hello world!'"


@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)




@app.route('/lab04')
def lab04_bootstrap():
    return app.send_static_file('lab04_bootstrap.html')

@app.route('/crash')
def crash():
    return 1/0

# lab10--------------------------------------------------------------------------------------------------------------------
@app.route("/lab10/contacts")
@login_required
def lab10_db_contacts():
        # db_contacts = Contact.query.all()
    db_contacts = PrivateContact.query.filter(
        PrivateContact.owner_id == current_user.id)
    contacts = []

    db_contacts = Contact.query.all()

    contacts = list(map(lambda x: x.to_dict(), db_contacts))
    app.logger.debug("DB Contacts: " + str(contacts))

    return jsonify(contacts)

@app.route('/lab10', methods=('GET', 'POST'))
def lab10_phonebook():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['firstname', 'lastname', 'phone']


        # validate the input
        for key in result:
            app.logger.debug(key, result[key])
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value


        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id_: create contact
            if not id_:
                validated_dict['owner_id'] = current_user.id
                # entry = Contact(**validated_dict)
                entry = PrivateContact(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
            # if there is an id_ already: update contact
            else:
                # contact = Contact.query.get(id_)
                contact = PrivateContact.query.get(id_)
                if contact.owner_id == current_user.id:
                    contact.update(**validated_dict)

            db.session.commit()


        return lab10_db_contacts()
    return app.send_static_file('lab10_phonebook.html')

@app.route('/lab10/remove_contact', methods=('GET', 'POST'))
def lab10_remove_contacts():
    app.logger.debug("LAB10 - REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            contact = Contact.query.get(id_)
            db.session.delete(contact)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return lab10_db_contacts()


# lab11--------------------------------------------------------------------------------------------------------------------
@app.route("/lab11/contacts")
def lab11_db_contacts():
    blog_entries = []
    db_contacts = BlogEntry.query.all()

    blog_entries = list(map(lambda x: x.to_dict(), db_contacts))
    app.logger.debug("DB Contacts: " + str(blog_entries))

    return jsonify(blog_entries)


@app.route('/lab11', methods=('GET', 'POST'))
def lab11_micro():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'message', 'email','date_Created','date_Update']


        # validate the input
        for key in result:
            app.logger.debug(key, result[key])
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value


        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id: create a new contact entry
            if not id_:
                entry = BlogEntry(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
            # if there is an id already: update the contact entry
            else:
                contact = BlogEntry.query.get(id_)
                contact.update(**validated_dict)


            db.session.commit()


        return lab11_db_contacts()
    return app.send_static_file('lab11_microblog.html')

@app.route('/lab11/remove_contact', methods=('GET', 'POST'))
def lab11_remove_contacts():
    app.logger.debug("LAB11 - REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            contact = BlogEntry.query.get(id_)
            db.session.delete(contact)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return lab11_db_contacts()

@app.route('/lab11/edit', methods=['POST'])
def lab11_edit():
    id = request.form.get('id')
    new_message = request.form.get('message')
    updatetime = request.form.get('date_Update')
    item = BlogEntry.query.get(id)
    item.message = new_message
    item.date_Update = updatetime
    db.session.commit()
    return jsonify(success=True)


# lab12--------------------------------------------------------------------------------------------------------------------
@app.route('/lab12')
def lab12_index():
   return 'Lab12'



@app.route('/lab12/profile')
@login_required
def lab12_profile():
    return render_template('lab12/profile.html')




@app.route('/lab12/login', methods=('GET', 'POST'))
def lab12_login():
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))


        user = AuthUser.query.filter_by(email=email).first()
 
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('lab12_login'))


        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('lab12_profile')
        return redirect(next_page)


    return render_template('lab12/login.html')





@app.route('/lab12/signup', methods=('GET', 'POST'))
def lab12_signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
 
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']


        # validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()


            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('lab12_signup'))


            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256'),
                                avatar_url=avatar_url)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()


        return redirect(url_for('lab12_login'))
    return render_template('lab12/signup.html')


def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method='sha256')[-6:]
    color = hex(int('0xffffff', 0) -
                int('0x'+bgcolor, 0)).replace('0x', '')
    lname = ''
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]


    avatar_url = "https://ui-avatars.com/api/?name=" + \
        fname + "+" + lname + "&background=" + \
        bgcolor + "&color=" + color
    return avatar_url



@ app.route('/lab12/logout')
@login_required
def lab12_logout():
    logout_user()
    return redirect(url_for('lab12_index'))



    

