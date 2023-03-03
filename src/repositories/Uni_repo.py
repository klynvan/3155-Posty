from src.models.models import Uni
from src.models.models import db

class Uni_repo:
        """In memory database which is a simple list of Users"""

        def get_all_uni(self):
            """Simply return all users from the in-memory database"""
            return Uni.query.all()


        def create_uni(self, university_name, acronym):
            uni = Uni(uni_name=university_name, acronym = acronym)
            db.session.add(uni)
            db.session.commit()



_uni_repo = Uni_repo()

