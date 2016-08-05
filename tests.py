import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<input id="field-name" class="form-control" type="text" name="name">', result.data)
        
        #print "FIXME"

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form
        self.assertEqual(result.status_code, 200)
        self.assertNotIn('<input id="field-name" class="form-control" type="text" name="name">', result.data)
        self.assertIn(' <h2>Party Details</h2>', result.data)
        #print "FIXME"


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""


        self.client = app.test_client()
        app.config['TESTING'] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        #Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        #(uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get("/games")
        self.assertIn('Chess', result.data)
        self.assertIn('Bingo', result.data)

        # print "FIXME"


if __name__ == "__main__":
    unittest.main()
