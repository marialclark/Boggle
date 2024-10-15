from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up to be done before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """Ensures board is properly formed, information is in the session, 
        and HTML is displayed."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

            #Board formation related tests
            self.assertIsInstance(session['board'], list)
            self.assertGreater(len(session['board']), 0)
            for row in session['board']:
                self.assertIsInstance(row, list)
                self.assertEqual(len(row), len(session['board'][0]))

            #Ensures session variables are set correctly
            self.assertIn('board', session)
            self.assertIn('games_played', session)
            self.assertIn('highest_score', session)

            #Checks initial values for games played & highscore
            self.assertEqual(session['games_played'], 0)
            self.assertEqual(session['highest_score'], 0)
            
    def test_valid_guess(self):
        """Tests functionality if a submitted guess is valid."""
        with self.client as client:
            board = [['J', 'R', 'D', 'M', 'W'], 
                     ['Q', 'K', 'T', 'I', 'T'], 
                     ['F', 'M', 'Y', 'U', 'F'], 
                     ['H', 'D', 'Z', 'J', 'P'], 
                     ['J', 'E', 'S', 'H', 'I']]
            with client.session_transaction() as session:
                session['board'] = board

            response = client.post('/submit-guess', json={'guess': 'FIT'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'ok'})

    def test_guess_not_on_board(self):
        """Tests functionality if a submitted guess is valid english but not
        present on the current Boggle board."""
        with self.client as client:
            board = [['J', 'R', 'D', 'M', 'W'], 
                     ['Q', 'K', 'T', 'I', 'T'], 
                     ['F', 'M', 'Y', 'U', 'F'], 
                     ['H', 'D', 'Z', 'J', 'P'], 
                     ['J', 'E', 'S', 'H', 'I']]
            with client.session_transaction() as session:
                session['board'] = board

            response = client.post('/submit-guess', json={'guess': 'HAT'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'not-on-board'})

    def test_guess_invalid(self):
        """Tests functionality if a submitted word in not valid english."""
        with self.client as client:
            board = [['J', 'R', 'D', 'M', 'W'], 
                     ['Q', 'K', 'T', 'I', 'T'], 
                     ['F', 'M', 'Y', 'U', 'F'], 
                     ['H', 'D', 'Z', 'J', 'P'], 
                     ['J', 'E', 'S', 'H', 'I']]
            with client.session_transaction() as session:
                session['board'] = board
            
            response = client.post('/submit-guess', json={'guess': 'asdf'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'result': 'not-word'})

    def test_score_display(self):
        """Tests that the score is being displayed on DOM."""
        with self.client as client:
            response = client.post('/score', json={'score': '21'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'Current Score:': '21'})

    def test_statistics(self):
        """Tests different session and highscore outcomes."""
        with self.client as client:
            #Sets initial session values
            with client.session_transaction() as session:
                session['games_played'] = 0
                session['highest_score'] = 15
            
            #Tests that there are new session stats after a new game with a 
            #new highscore
            response = client.post('/update-stats', json={'score': 20})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['games_played'], 1)
            self.assertEqual(response.json['highest_score'], 20)

            with client.session_transaction() as session:
                self.assertEqual(session['games_played'], 1)
                self.assertEqual(session['highest_score'], 20)

            #Tests that the highscore goes unchanged when new user score is lower.
            response = client.post('/update-stats', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['games_played'], 2)
            self.assertEqual(response.json['highest_score'], 20)

            with client.session_transaction() as session:
                self.assertEqual(session['games_played'], 2)
                self.assertEqual(session['highest_score'], 20)

            #Tests new stats when new game results in same highscore.
            response = client.post('/update-stats', json={'score': 20})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['games_played'], 3)
            self.assertEqual(response.json['highest_score'], 20)

            with client.session_transaction() as session:
                self.assertEqual(session['games_played'], 3)
                self.assertEqual(session['highest_score'], 20)
