from src.models.models import db
from src.models.models import User_
from src.models.models import Comment
from src.models.models import Like_
from src.models.models import Post

class User_Repository:

    def get_all_users(self):
        # TODO get all users from the DB
        return User_.query.all()

    def get_user_by_id(self, user_id):
        # TODO get a single user from the DB using the ID
        user = User_.query.get(user_id)
        return user

    def create_user(self, first_name, last_name, username, email, user_password, university):
        # TODO create a new User in the DB

        new_user = User_(first_name = first_name, last_name = last_name, username = username, email = email, user_password = user_password, university=university)
        db.session.add(new_user)
        db.session.commit()

        return None


    def edit_user(self, user_id, first_name, last_name, username, email, university):
        # TODO create a new User in the DB

        user = self.get_user_by_id(user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.university = university

        db.session.commit()

        return None

    def change_password(self, user_id, new_password):
        user = self.get_user_by_id(user_id)
        user.user_password = new_password
        db.session.commit()


    def get_user_by_username(self, username):
        return User_.query.filter_by(username = username).first()

    def search_users(self, title):
        # TODO get all Users matching case insensitive substring (SQL LIKE, use google for how to do with SQLAlchemy)
        return None

    def set_profile_pic(self, user_id, profile_pic_url):
        user = self.get_user_by_id(user_id)
        user.avatar_url = profile_pic_url
        db.session.commit()


    def delete_user(self, user_id):
        #delete all posts and comments by user
        #should cascade delete all chidren comments as well
        user = self.get_user_by_id(user_id)

        comments = Comment.query.filter_by(user_id=user_id).all()

        #delete all comments associated with post
        for comment in comments:
            #get all the children comments of this ocmmmnet
            child_comments = Comment.query.filter_by(parent_comment_id=comment.comment_id).all()
            for child_comment in child_comments:
                db.session.delete(child_comment)

            db.session.delete(comment)

        posts = Post.query.filter_by(user_id=user_id).all()
        for post in posts:
            #delete all posts by user and comments on that post
            comments = Comment.query.filter_by(post_id = post.post_id).all()
            for comment in comments:
                db.session.delete(comment)
            db.session.delete(post)

        #delete all likes asscoiated with the post
        likes = Like_.query.filter_by(user_id=user_id).all()

        for like in likes:
            db.session.delete(like)

        db.session.delete(user)

        db.session.commit()



# Singleton to be used in other modules
user_repository_singleton = User_Repository()
