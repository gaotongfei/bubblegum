import unittest
from app import db, create_app
from app.models import User


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='test')
        # db.session.add(u)
        # db.commit()
        self.assertTrue(u.password_hash is not None)
    '''
    def test_password_getter(self):
        u = User(password='test')
        with self.assertRaises(AttributeError):
            u.password
    '''

    def test_insert_data(self):
        u = User(username='test', email='test@test.com', password='test')
        db.session.add(u)
        db.session.commit()
        query_user = User.query.filter_by(username='test').first()
        self.assertEqual(query_user.email, 'test@test.com')

