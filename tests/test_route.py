from flask.testing import FlaskClient
from src.models.models import User_, Post, db
from app import app


def test_create_user_and_post(test_app: FlaskClient):
    with app.app_context():

        #creating user and post and seeing if it displays
        test_user = User_(first_name = "first-name", last_name = "last-name", username = "example-username", email = "example@uncc.edu", user_password = "password", university="UNCC", user_id =999)
        db.session.add(test_user)
        db.session.commit()


        test_post = Post(university="UNCC", post_title="post-title",post_text="post-text", user_id=test_user.user_id)
        db.session.add(test_post)
        db.session.commit()


        res = test_app.get('/index')
        page_data = res.data

        assert res.status_code == 200
        assert b'<h6 class="fw-bold text-primary mb-1">example-username | UNCC</h6>' in page_data

        db.session.delete(test_post)
        db.session.delete(test_user)
        db.session.commit()