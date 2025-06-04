import unittest
from app import app

class SmartHealthAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json())
        self.assertEqual(response.get_json()['status'], 'healthy')

    def test_analyze_missing_fields(self):
        response = self.client.post('/api/analyze', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_analyze_valid(self):
        data = {
            'name': 'Test User',
            'description': 'I have a headache and feel nauseous.',
            'symptoms[]': ['headache', 'nausea'],
            'body_parts[]': ['head']
        }
        response = self.client.post('/api/analyze', data=data, headers={
            'X-Requested-With': 'XMLHttpRequest'
        })
        json_data = response.get_json()
        self.assertIsNotNone(json_data)
        self.assertIn('possible_conditions', json_data)

if __name__ == '__main__':
    unittest.main()
