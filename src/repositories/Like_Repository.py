from src.models.models import db
from src.models.models import Like_


class Like_Repository:

    def get_all_likes(self):
        # TODO get all likes from the DB
        return Like_.query.all()

    def get_like_by_id(self, like_id):
        # TODO get a single like from the DB using the ID
        return Like_.query.get(like_id)

    def like_exists(self, user_id, post_id):

        like = Like_.query.filter_by(user_id = user_id, post_id = post_id).first()

        if(like == None):
            return False

        return True

    def get_like(self, user_id, post_id):
        like = Like_.query.filter_by(user_id = user_id, post_id = post_id).first()
        return like


    def get_likes_by_user_id(self, user_id):
        # TODO get likes from the DB using th user_ID, all the likes by a user
        return Like_.query.get(user_id)

    def get_likes_by_post_id(self, post_id):
        # TODO get likes from the DB using the post_ID, all the likes on a post
        return Like_.query.get(post_id)

    def create_like(self, post_id, user_id):
        # TODO if like doesn't exist create it, otherwise destroy it
        #returns true if like was created
        #returns false if like was destroyed

        if(not self.like_exists(user_id, post_id)):
            new_like = Like_(post_id=post_id, user_id=user_id)
            db.session.add(new_like)
            db.session.commit()

            return True

        else:
            like = self.get_like(user_id, post_id)
            db.session.delete(like)
            db.session.commit()

            return False

        

# Singleton to be used in other modules
like_repository_singleton = Like_Repository()
