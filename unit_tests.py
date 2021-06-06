import json
from flask import Flask
import unittest
from case import app, db, Urls
from functions import check_short, check_short2

app.testing = True


class TestApi(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.app = Flask("test")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
        db.init_app(self.app)
        db.create_all()

        test_url = Urls(url="https://www.facebook.com", shortcode="facbok", created_date="2021-12-21",
                        last_redirect="2021-12-21", redirect_count=1)
        db.session.add(test_url)
        db.session.commit()

    def tearDown(self):

        # Ensures that the database is emptied for next unit test
        db.session.remove()
        db.drop_all()

    def test_get_url(self):
        with app.test_client() as client:
            result = client.get('/facbok')
            self.assertTrue("https://www.facebook.com" in str(result.data))

    def test_get_stats(self):
        with app.test_client() as client:
            result = client.get('/facbok/stats')
            self.assertEqual({"lastRedirect": "2021-12-21", "RedirectCount": 1, "createdDate": "2021-12-21"},
                             json.loads(result.data))

    def test_wrong_start_url(self):
        with app.test_client() as client:
            expected = {"message": "The provided url is invalid"}
            # send data as POST form to endpoint
            sent = json.dumps({'url': 'www.hotel.it', 'shortcode': 'jukola'})
            result = client.post(
                '/shorten',
                data=sent
            )
            # check result from server with expected data
            result = json.loads(result.data)
            self.assertEqual(
                result,
                expected
            )

    def test_url_is_none(self):
        with app.test_client() as client:
            expected = {"message": "Url not present"}
            # send data as POST form to endpoint
            sent = json.dumps({'shortcode': 'jukola'})
            result = client.post(
                '/shorten',
                data=sent
            )
            # check result from server with expected data
            result = json.loads(result.data)
            self.assertEqual(
                result,
                expected
            )

    def test_shortcode_is_different(self):
        with app.test_client() as client:
            expected = {"message": "The provided shortcode is invalid"}
            # send data as POST form to endpoint
            sent = json.dumps({'url': 'https://www.hotel.it', 'shortcode': 'jukol$'})
            result = client.post(
                '/shorten',
                data=sent
            )
            # check result from server with expected data
            result = json.loads(result.data)
            self.assertEqual(
                result,
                expected
            )

    def test_shortcode_is_longer(self):
        with app.test_client() as client:
            expected = {"message": "The provided shortcode is invalid"}
            # send data as POST form to endpoint
            sent = json.dumps({'url': 'https://www.hotel.it', 'shortcode': 'jukolaaaa'})
            result = client.post(  
                '/shorten',
                data=sent
            )
            # check result from server with expected data
            result = json.loads(result.data)
            self.assertEqual(
                result,
                expected
            )

    def test_shortcode_is_correct(self):
        with app.test_client() as client:
            expected = {"shortcode": "jukola"}
            # send data as POST form to endpoint
            sent = json.dumps({'url': 'https://www.hotel.it', 'shortcode': 'jukola'})
            result = client.post(  
                '/shorten',
                data=sent
            )
            # check result from server with expected data
            result = json.loads(result.data)
            self.assertEqual(
                result,
                expected
            )

    def test_length_is_6(self):
        shortcode = 'hola12'
        self.assertTrue(check_short(shortcode))

    def test_length_is_not_6(self):
        shortcode = 'hola123'
        self.assertFalse(check_short(shortcode))

    def test_pattern_is_valid(self):
        shortcode = 'Cava12'
        self.assertTrue(check_short(shortcode))

    def test_pattern_is_not_valid(self):
        shortcode = 'Cava1$'
        self.assertFalse(check_short(shortcode))

    def test_shortcode_present(self):
        db_row = 'lolare'
        self.assertTrue(check_short2(db_row))

    def test_shortcode_not_present(self):
        db_row = None
        self.assertFalse(check_short2(db_row))


if __name__ == '__main__':
    unittest.main()
