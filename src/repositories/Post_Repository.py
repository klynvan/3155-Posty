from src.models.models import db
from src.models.models import Post
from src.models.models import Comment
from src.models.models import Like_


class Post_Repository:

    def get_all_posts(self):
        # TODO get all posts from the DB
        return Post.query.all()

    def get_post_by_id(self, post_id):
        # TODO get a single user from the DB using the ID
        return Post.query.get(post_id)

    def create_post(self, university, post_title, post_text, user_id):

        new_post = Post(university=university, post_title=post_title,
                        post_text=post_text, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return new_post

    def search_posts(self, post_title):
        # TODO get all Users matching case insensitive substring (SQL LIKE, use google for how to do with SQLAlchemy)
        return Post.query.filter_by(post_title=post_title).first()

    def returnAllComments(self, post_id):
        # TODO return all comments assoicated witht that post ID

        comments = Comment.query.filter_by(post_id=post_id).all()

        return comments


    def delete_post(self, post_id):

        comments = Comment.query.filter_by(post_id=post_id).all()

        #delete all comments associated with post
        for comment in comments:
            db.session.delete(comment)

        #delete all likes asscoiated with the post
        likes = Like_.query.filter_by(post_id=post_id).all()

        for like in likes:
            db.session.delete(like)


        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()

    def increment_num_likes(self, post_id):
        post = Post.query.get(post_id)
        post.number_likes += 1
        db.session.commit()

    def decrement_num_likes(self, post_id):
        post = Post.query.get(post_id)
        post.number_likes -=1
        db.session.commit()


    def edit_post(self, post_id, post_title, post_text):
        post = self.get_post_by_id(post_id)
        post.post_title = post_title
        post.post_text = post_text
        db.session.commit()


# Singleton to be used in other modules
post_repository_singleton = Post_Repository()
