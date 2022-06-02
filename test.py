from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Stuff to do before every test"""

        #setup a test client for the app to use for the tests
        self.client = app.test_client()
        #configure the app so it knows we are running tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            # get the homepage of the client to use for our response data
            response = self.client.get('/')
            #confirm there is a 'board' in session
            self.assertIn('board', session)
            #passes if there is no 'highscore' in session since this is a fresh game
            self.assertIsNone(session.get('highscore'))
            #passes if nplays is not in the session
            self.assertIsNone(session.get('nplays'))
            #passes if this string is in response data
            self.assertIn(b'<p>High Score:', response.data)
            #passes if this string is in response data
            self.assertIn(b'Score:', response.data)
            #passes if this string is in response data
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            #set the test client with a new custom board for testing the session
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        #set the response of the client using the check-word query set to 'cat' which should return jsonify ok and store it as a variable
        response = self.client.get('/check-word?word=cat')
        #run the test that passes if the result is ok
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        
        #Retrieve the root directory
        self.client.get('/')
        #Set the response client to be a word that is too long to be on the board and not on the board
        response = self.client.get('/check-word?word=impossible')
        #Passes if the response is html result not-on-board
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        #Set the root directory
        self.client.get('/')
        #use check-word query set to be gibberish
        response = self.client.get('/check-word?word=guaplkjchina')
        #Passes if the result returns not-word
        self.assertEqual(response.json['result'], 'not-word')