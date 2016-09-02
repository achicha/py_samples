from flask_testing import TestCase

from project import app, db
from project.models import User, BlogPost


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.add(BlogPost("Test post", "This is a test. Only a test."))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask!', response.data)

    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'This is a test. Only a test.', response.data)

    def test_correct_credentials(self):
        response = self.client.post('/login',
                                    data=dict(username='admin', password='admin'),
                                    follow_redirects=True)
        self.assertIn(b'You were logged in', response.data)

    def test_incorrect_credentials(self):
        response = self.client.post('/login',
                                    data=dict(username='admin123', password='admin123'),
                                    follow_redirects=True)
        self.assertIn(b'Invalid Credentials', response.data)

    def test_logout(self):
        self.client.post('/login',
                         data=dict(username='admin', password='admin'),
                         follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)
