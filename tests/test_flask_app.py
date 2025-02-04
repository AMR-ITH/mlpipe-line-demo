import unittest
from flask_app import app

class FalskAppTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        """
        cls.client = app.test_client(): This line creates a test client for the Flask application app and assigns it to cls.client. 
        The test client is used to simulate requests to the Flask application without running a live server.
          This allows you to test your routes and logic in a controlled environment.
        """

        cls.client = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Sentiment Analysis</title>', response.data)

    def test_predict(self):
        response = self.app.post('/predict',data={'text': 'I love this!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
             b'Happy' in response.data or b'Sad' in response.data,
            "Response should contain either 'Happy' or 'Sad'"
        )
if __name__ == '__main__':
    unittest.main()
