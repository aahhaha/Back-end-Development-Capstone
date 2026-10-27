from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from django.utils import timezone
from concert.models import Concert, ConcertAttending

class ConcertViewsTests(TestCase):
    def test_public_pages(self):
        for url in ['/', '/login/', '/signup/', '/concerts/', '/admin/login/']:
            self.assertEqual(self.client.get(url).status_code, 200)

    @patch('concert.views.requests.get')
    def test_microservice_pages(self, get):
        get.return_value.json.return_value = {'songs': [{'id': 1, 'title': 'Example', 'lyrics': 'Lyrics'}]}
        self.assertContains(self.client.get('/songs/'), 'Example')
        get.return_value.json.return_value = [{'pic_url': '/static/images/img.jpeg', 'event_date': '2030-01-01', 'event_city': 'Astana'}]
        self.assertContains(self.client.get('/photos/'), 'Astana')

    def test_attendance_is_user_scoped(self):
        concert = Concert.objects.create(concert_name='Live', duration=2, city='Astana', date=timezone.now())
        User.objects.create_user('listener', password='development-test-pass')
        self.client.login(username='listener', password='development-test-pass')
        response = self.client.post('/concert_attendee/', {'concert_id': concert.id, 'attendee_choice': 'Attending'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConcertAttending.objects.get().attending, 'Attending')
        self.client.post('/concert_attendee/', {'concert_id': concert.id, 'attendee_choice': 'invalid'})
        self.assertEqual(ConcertAttending.objects.get().attending, 'Attending')
