import unittest
from app import app, users_db, expressions_db  # Import app, users_db, and expressions_db
from werkzeug.security import generate_password_hash

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Set up a test user in users_db
        users_db['test@example.com'] = generate_password_hash('test123')

    def tearDown(self):
        # Clean up the test user and any other test data
        users_db.pop('test@example.com', None)
        expressions_db.clear()


    def test_login(self):
        response = self.app.post('/login', data=dict(email='test@example.com', password='test123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Add additional assertions based on your login logic
    def test_logout(self):
        # First, log in
        self.app.post('/login', data=dict(email='test@example.com', password='test123'), follow_redirects=True)

        # Then, log out
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Add additional assertions based on your logout logic

    def test_evaluate_expression(self):
        # Ensure the user is logged in
        self.app.post('/login', data=dict(email='test@example.com', password='test123'), follow_redirects=True)
        # Test expression evaluation
        response = self.app.post('/evaluate', data=dict(expression='2+2'), follow_redirects=True)
        self.assertIn(b'2+2 = 4', response.data)
        # Add additional assertions if needed
    def test_view_history(self):
        # Ensure the user is logged in
        self.app.post('/login', data=dict(email='test@example.com', password='test123'), follow_redirects=True)

        # Add an expression to the history
        self.app.post('/evaluate', data=dict(expression='3*3'), follow_redirects=True)

        # Test viewing history
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'3*3 = 9', response.data)
        # Add additional assertions based on your application's logic
if __name__ == '__main__':
    unittest.main()
