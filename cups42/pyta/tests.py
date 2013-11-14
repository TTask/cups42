from django.test import TestCase
from models import UserInfo
from models import RequestHistoryEntry
import views
from django.core.urlresolvers import reverse
import random
import re
from BeautifulSoup import BeautifulSoup


class TestIndexView(TestCase):
    
    def setUp(self):
        fixtures = ['initial_data.json']
        self.user = UserInfo.objects.get(pk=1)

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.user.name in response.content)
        self.assertTrue(self.user.surname in response.content)
        self.assertTrue(str(self.user.birth_date) in response.content)
        self.assertTrue(str(self.user.bio) in response.content)
        self.assertTrue(self.user.contact_phone in response.content)
        self.assertTrue(str(self.user.contact_email) in response.content)
        self.assertTrue(str(self.user.contact_jabber) in response.content)
        self.assertTrue(self.user.contact_skype in response.content)
        self.assertTrue(self.user.contact_other in response.content)


class TestREquestHistoryView(TestCase):
    def setUp(self):
        self.request_path = reverse('home')

    def test_history_entry_creation(self):
        self.client.get(self.request_path)
        entry = RequestHistoryEntry.objects.all()[:1][0]
        self.assertEqual(self.request_path, entry.request_path)

    def test_history_page(self):
        requests_limit = 10
        request_path_done = []          #this is requests done by test
        request_paths = [reverse('home'), reverse('requests')]
        while requests_limit > 0:
            request = random.choice(request_paths)
            request_path_done.append(request)
            requests_limit-=1
            self.client.get(request)
        response = self.client.get(reverse('requests'))
        sp = BeautifulSoup(response.content)
        requests_table_onpage = [elem.getText() for elem in sp.findAll('td', {'class': 'request-path'})]
        self.assertEqual(request_path_done, requests_table_onpage)
