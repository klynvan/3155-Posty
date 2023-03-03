from src.models.models import db
from src.models.models import Repost


class Repost_Repository:

    def get_all_reposts(self):
        # TODO get all reposts from the DB
        return Repost.query.all()

    def get_repost_by_id(self, repost_id):
        # TODO get a single repost from the DB using the ID
        return Repost.query.get(repost_id)

    def get_reposts_by_user_id(self, user_id):
        # TODO get reposts from the DB using th user_ID, all the repposts by a user
        return Repost.query.get(user_id)

    def get_reposts_by_post_id(self, post_id):
        # TODO get reposts from the DB using the post_ID, all the reposts on a post

        return Repost.query.get(post_id)

    def create_repost(self, reposter_user_id, post_id, poster_user_id):
        # TODO create a new repost in the DB
        new_repost = Repost(reposter_user_id=reposter_user_id,
                            post_id=post_id, poster_user_id=poster_user_id)
        db.session.add(new_repost)
        db.session.commit()
        return new_repost


# Singleton to be used in other modules
repost_repository_singleton = Repost_Repository()
