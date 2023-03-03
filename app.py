from flask_login import current_user
from flask_login import LoginManager
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import os
from PIL import Image


from src.repositories.Post_Repository import post_repository_singleton
from src.repositories.User_Repository import user_repository_singleton
from src.repositories.Comment_Repository import comment_repository_singleton
from src.repositories.Like_Repository import like_repository_singleton
from src.repositories.Uni_repo import _uni_repo
from src.models.models import Post
from src.models.models import User_

from src.models.models import db

app = Flask(__name__)  # __name__ refers to the module name
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default = 'postgresql://postgres:password@localhost:5432/posty_database')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/posty_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


global post_list
post_list = post_repository_singleton.get_all_posts()
global uni_list
uni_list = _uni_repo.get_all_uni()

# login stuff
"""
global logged_in 
logged_in = False
global current_user
current_user = None
"""

# new loggin stuff
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')  # Python decorator, new syntax
def index():
    uni_list = _uni_repo.get_all_uni()
    post_list = post_repository_singleton.get_all_posts()

    post_list = sorted(post_list, key = lambda post: post.number_likes)
    post_list.reverse()
    return render_template("index.html", current_user = current_user, post_list= post_list)


@app.route('/index')  # Python decorator, new syntax
def go_to_index():
    uni_list = _uni_repo.get_all_uni()
    post_list = post_repository_singleton.get_all_posts()

    post_list = sorted(post_list, key = lambda post: post.number_likes)
    post_list.reverse()
    return render_template("index.html", current_user = current_user, post_list= post_list)



@app.route('/login_page')  # Python decorator, new syntax
def login_page():
    return render_template("login_page.html", current_user=current_user)


@app.route('/home_page')  # Python decorator, new syntax
def home_page():
    uni_list = _uni_repo.get_all_uni()
    post_list = post_repository_singleton.get_all_posts()

    post_list = sorted(post_list, key = lambda post: post.number_likes)
    post_list.reverse()
    print(post_list)
    return render_template("index.html", current_user = current_user, post_list= post_list)



@app.route('/sign_up_page')  # Python decorator, new syntax
def sign_up_page():
    return render_template("sign_up_page.html", current_user=current_user, uni_list = uni_list)


@app.route('/account_info_page')  # Python decorator, new syntax
def account_info_page():
    uni_list = _uni_repo.get_all_uni()
    return render_template("account_info.html", current_user=current_user, uni_list = uni_list)


@app.route('/create_new_post_page')  # Python decorator, new syntax
def create_new_post_page():

    if (current_user == None):
        # need to be logged in to make posts
        return index()

    return render_template("create_new_post.html", current_user=current_user)


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    flash("must be logged in to do that")
    return redirect(url_for('login_page'))


@app.post('/sign_up')  # Python decorator, new syntax
def sign_up():
    # code to validate and add user to database goes here
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    user_university = request.form.get('comp_select')
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_repeat_password = request.form.get('repeat_password')

    # if passwords don't match redirect
    if (user_password != user_repeat_password):
        # TODO: handle this
        flash('Password Does Not Match')
        return sign_up_page()

    # if this returns a user, then the email already exists in database
    user = User_.query.filter_by(email=user_email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return sign_up_page()

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    user_repository_singleton.create_user(firstname, lastname, username, user_email, generate_password_hash(
        user_password, method='sha256'), user_university)

    flash('Form Submitted Successfully')

    return login_page()





@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User_.query.get(int(user_id))


@app.post('/login')  # Python decorator, new syntax
def login():


    username = request.form.get('username')
    password = request.form.get('password')

    user = User_.query.filter_by(username=username).first()
    

    # login code goes here
    session["username"] = user.username



    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.user_password, password):
        flash('Please check your login details and try again.')
        # if password details don't match reload the page
        return login_page()

    # if the above check passes, then we know the user has the right credentials
    login_user(user)

    print("logged in :" + current_user.username)

    # if the above check passes, then we know the user has the right credentials
    return index()


@app.post('/logout')
@login_required
def logout():
    session.pop("user", None)
    logout_user()
    return index()




@app.post('/create_new_post')  # Python decorator, new syntax
@login_required
def create_new_post():
    if "username" in session:
        user = session["username"]

        global post_list

        title = request.form.get('title')
        post_text = request.form.get('post')

        if (current_user.is_authenticated):

            post_repository_singleton.create_post(
                current_user.university, title, post_text, current_user.user_id)
            # update post list
            post_list = post_repository_singleton.get_all_posts()

        return redirect(url_for('go_to_index'))

    else:
        return redirect(url_for('login_page'))


@app.route('/edit_post_page/<int:post_id>')  # Python decorator, new syntax
@login_required
def edit_post_page(post_id):
    user_post = post_repository_singleton.get_post_by_id(post_id)
    return render_template("edit_post.html", post = user_post)

@app.post('/edit_post/<int:post_id>')  # Python decorator, new syntax
@login_required
def edit_post(post_id):
    user_post = post_repository_singleton.get_post_by_id(post_id)

    title = request.form.get('title')
    post_text = request.form.get('post')
    post_repository_singleton.edit_post(post_id,title,post_text)

    return redirect(url_for("post_viewer", post_id=post_id))

"""
@app.post('/logout') # Python decorator, new syntax
def logout():
    global current_user

    current_user = None

    return redirect("/")
"""



#view single post with its ocmments

@app.route('/post_viewer/<int:post_id>')
def post_viewer(post_id):
    global post_list

    selected_post_id = post_id

    # grabbing posts using post ids
    user_post = None

    for post in post_list:
        if (str(selected_post_id) == str(post.post_id)):
            user_post = post

    user_post = post_repository_singleton.get_post_by_id(post_id)

    if (user_post == None):
        return index()

    # need to find list of all comments associated with this particular post and pass that into render tempate
    comments = post_repository_singleton.returnAllComments(selected_post_id)
    print(comments)

    # if the comments list is empty display the page
    if (len(comments) == 0):
        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={})

    # organize comments list into a dictionary where
    # {  parents comment: [child comment 1, child comment 2, child comment 3]   }

    comment_dictionary = generate_comment_dictionary(post_id)

    print(comment_dictionary)

    return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=False)



#pop up a text box to add comment
@app.route('/comment_text_area/<int:post_id>')
@login_required
def post_viewer_comment_text_area(post_id):

    # get post object using id
    user_post = post_repository_singleton.get_post_by_id(post_id)

    # get comment dictionary
    comment_dictionary = generate_comment_dictionary(post_id)

    # can't comment if not logged in
    if (not current_user.is_authenticated):
        # if the comments list is empty display the page
        if (len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=False)

        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=False)

    # if the comments list is empty display the page
    if (len(comment_dictionary) == 0):
        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=True)

    return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=True)



#pop up a text box to edit parent ocmmment
@app.route('/edit_parent_comment_text_area/<int:post_id>/<int:comment_id>')
@login_required
def post_viewer_parent_comment_edit_text_area(post_id,comment_id):

    #get post object using id
    user_post = post_repository_singleton.get_post_by_id(post_id)
    comment = comment_repository_singleton.get_comment_by_id(comment_id)

    #get comment dictionary
    comment_dictionary = generate_comment_dictionary(post_id)

    del comment_dictionary[comment]

    #can't comment if not logged in
    if(not current_user.is_authenticated):
        #if the comments list is empty display the page
        if(len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = {}, parent_comment=False)

        return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, parent_comment= False)

    #if the comments list is empty display the page
    if(len(comment_dictionary) == 0):
        return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = {}, parent_comment_edit=True, comment_to_edit = comment)

    return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, parent_comment_edit= True, comment_to_edit = comment)
    


#edit parent comment
@app.route('/edit_parent_comment/<int:post_id>/<int:comment_id>')
@login_required
def post_viewer_parent_comment_edit(post_id,comment_id):
    comment_text = request.args.get('comment_text')
    comment_repository_singleton.edit_comment(comment_id,comment_text)
    return redirect(url_for("post_viewer", post_id=post_id))



#post commment
@app.route('/comment_text_area/comment/<int:post_id>')
@login_required
def post_viewer_comment(post_id):

    comment_dictionary = generate_comment_dictionary(post_id)
    user_post = post_repository_singleton.get_post_by_id(post_id)

    # can't comment if not logged in
    if (not current_user.is_authenticated):
        # if the comments list is empty display the page
        if (len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=False)

        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=False)

    comment_text = request.args.get('comment_text')

    comment_repository_singleton.create_parent_comment(
        comment_text, post_id, current_user.user_id)
    comment_dictionary = generate_comment_dictionary(post_id)

    return redirect(url_for("post_viewer", post_id=post_id))


#pop up text area to add child comment
@app.route('/comment_text_area/<int:post_id>/<int:comment_id>')
@login_required
def post_viewer_reply_to_comment(post_id, comment_id):

    # get post object using id
    user_post = post_repository_singleton.get_post_by_id(post_id)
    comment_to_reply = comment_repository_singleton.get_comment_by_id(
        comment_id)

    # get comment dictionary
    comment_dictionary = generate_comment_dictionary(post_id)

    # can't comment if not logged in
    if (not current_user.is_authenticated):
        # if the comments list is empty display the page
        if (len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=False)

        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=False)

    # if the comments list is empty display the page
    if (len(comment_dictionary) == 0):
        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=False)


    return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, parent_comment= False, comment_to_reply = comment_to_reply, comment_reply_bool = True)
    


#post child comment
@app.route('/comment_text_area/comment/<int:post_id>/<int:comment_id>')
@login_required
def post_viewer_comment_to_comment(post_id, comment_id):

    comment_dictionary = generate_comment_dictionary(post_id)
    print(comment_dictionary)
    user_post = post_repository_singleton.get_post_by_id(post_id)
    comment_to_reply = comment_repository_singleton.get_comment_by_id(
        comment_id)

    # can't comment if not logged in
    if (not current_user.is_authenticated):
        # if the comments list is empty display the page
        if (len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary={}, parent_comment=False)

        return render_template("post_viewer.html", current_user=current_user, post=user_post, comment_dictionary=comment_dictionary, parent_comment=False)

    comment_text = request.args.get('comment_text')
    comment_repository_singleton.create_child_comment(
        comment_text, post_id, current_user.user_id, comment_id)
    comment_dictionary = generate_comment_dictionary(post_id)


    """
    #if the comments list is empty display the page
    if(len(comment_dictionary) == 0):
        return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = {}, parent_comment=False)

    return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, parent_comment= False)
    """
    return redirect(url_for("post_viewer", post_id=post_id))


#pop up a text box to edit child comment
@app.route('/edit_child_comment_text_area/<int:post_id>/<int:parent_comment_id>/<int:comment_id>')
@login_required
def post_viewer_child_comment_edit_text_area(post_id, parent_comment_id, comment_id):

    #get post object using id
    user_post = post_repository_singleton.get_post_by_id(post_id)
    comment = comment_repository_singleton.get_comment_by_id(comment_id)
    parentcomment = comment_repository_singleton.get_comment_by_id(parent_comment_id)
    comment_to_reply = comment_repository_singleton.get_comment_by_id(parent_comment_id)

    #get comment dictionary
    comment_dictionary = generate_comment_dictionary(post_id)

    comment_dictionary[parentcomment].remove(comment)

    #can't comment if not logged in
    if(not current_user.is_authenticated):
        #if the comments list is empty display the page
        if(len(comment_dictionary) == 0):
            return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = {}, parent_comment=False)

        return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, parent_comment= False)

    #if the comments list is empty display the page
    if(len(comment_dictionary) == 0):
        return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = {}, child_comment_edit=True, comment_to_edit = comment)

    return render_template("post_viewer.html", current_user = current_user, post = user_post, comment_dictionary = comment_dictionary, child_comment_edit= True, comment_to_edit = comment, comment_to_reply = comment_to_reply)
    



def generate_comment_dictionary(selected_post_id):

    # organize comments list into a dictionary where
    # {  parents comment: [child comment 1, child comment 2, child comment 3]   }

    comments = post_repository_singleton.returnAllComments(selected_post_id)

    comment_dictionary = {}

    # parent comments
    for comment in comments:
        if comment.parent_comment_id == None:
            comment_dictionary[comment] = []

    # child comments
    for comment in comments:
        if comment.parent_comment_id != None:

            try:
                comment_dictionary[comment_repository_singleton.get_comment_by_id(
                    comment.parent_comment_id)].append(comment)
            except:
                print("hi")

    return comment_dictionary


@app.route('/delete_comment/<int:post_id>/<int:comment_id>')
@login_required
def delete_comment(comment_id, post_id):

    comment_repository_singleton.delete_comment(comment_id)

    return redirect(url_for('post_viewer', post_id=post_id))


@app.route('/delete_post_index/<int:post_id>')
@login_required
def delete_post_index(post_id):
    post_repository_singleton.delete_post(post_id)
    return redirect(url_for('go_to_index'))


@app.route('/delete_post_post_viewer/<int:post_id>')
@login_required
def delete_post_post_viewer(post_id):

    post_repository_singleton.delete_post(post_id)

    return redirect(url_for('go_to_index'))


@app.route('/like/<int:post_id>')
@login_required
def like(post_id):

    # creating like and incrementing number of likes on post
    like_created = like_repository_singleton.create_like(
        post_id, current_user.user_id)

    if (like_created):
        post_repository_singleton.increment_num_likes(post_id)
    else:
        post_repository_singleton.decrement_num_likes(post_id)

    return redirect(url_for('post_viewer', post_id=post_id))


@app.route('/index_like/<int:post_id>')
@login_required
def index_like(post_id):

    # creating like and incrementing number of likes on post
    like_created = like_repository_singleton.create_like(
        post_id, current_user.user_id)

    if (like_created):
        post_repository_singleton.increment_num_likes(post_id)
    else:
        post_repository_singleton.decrement_num_likes(post_id)

    return redirect(url_for('go_to_index'))


UPLOAD_FOLDER = './static/images/profiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()

# uploading pfp


@app.route('/uploads/pp/', methods=['GET', 'POST'])
@login_required
def upload_photo():

    if request.method == 'POST' and 'photo' in request.files:

        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            # assign the member unique id as the file name for our uploaded image
            # we are also getting some URLs to the image we will use in our profile.html file
            profilepic_name = str(current_user.username) + \
                "."+extension(file.filename)
            profilepic_url = 'images/profiles/'+profilepic_name
            workingdir = os.path.abspath(os.getcwd())
            fullprofilepic_url = workingdir + profilepic_url

            # if filename already exists delete it
            if os.path.isfile(fullprofilepic_url) == True:
                os.remove(fullprofilepic_url)

            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], profilepic_name))

            flash("Success! Profile photo uploaded successfully.", 'success')

            # save the image url on database for futire use
            user_repository_singleton.set_profile_pic(
                current_user.user_id, profilepic_url)
            return redirect(url_for('go_to_index'))

    return redirect(url_for('go_to_index'))


@app.post('/edit_profile')
@login_required
def edit_profile():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    user_university = request.form.get('comp_select')
    if user_university is None:
        user_university = current_user.university

    user_email = request.form.get('email')

    user_repository_singleton.edit_user(current_user.user_id, firstname, lastname, username, user_email, user_university)


    return redirect(url_for('account_info_page'))

@app.post('/change_password')
@login_required
def change_password():
    curr_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    repeat_new_password = request.form.get('repeat_new_password')

    print(curr_password)
    print(new_password)
    print(repeat_new_password)

    if not check_password_hash(current_user.user_password, curr_password):
        flash('incorresct password')
        #if password details don't match reload the page
        redirect(url_for('account_info_page'))

    #if passwords don't match redirect
    if (new_password != repeat_new_password):
        # TODO: handle this
        flash('new password Does Not Match')
        return redirect(url_for('account_info_page'))

    user_repository_singleton.change_password(current_user.user_id, generate_password_hash(new_password, method='sha256'))
    flash('password successfully changed')
    return redirect(url_for('account_info_page'))


@app.post('/delete_account')
@login_required
def delete_account():
    user_repository_singleton.delete_user(current_user.user_id)
    logout_user()
    return redirect(url_for('go_to_index'))


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
