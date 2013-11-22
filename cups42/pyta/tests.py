from django.test import TestCase
from django.core.urlresolvers import reverse
from models import UserInfo
from models import RequestHistoryEntry
from BeautifulSoup import BeautifulSoup
import views
import random


TEST_USER_LOGIN = 'admin'
TEST_USER_PASSWORD = 'admin'
TEST_FIXTURES = ['db_data.json']


class TestIndexView(TestCase):
    fixtures = TEST_FIXTURES

    def setUp(self):
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


class TestRequestHistoryView(TestCase):
    def setUp(self):
        self.request_path = reverse('home')

    def test_history_entry_creation(self):
        self.client.get(self.request_path)
        entry = RequestHistoryEntry.objects.all()[:1][0]
        self.assertEqual(self.request_path, entry.request_path)

    def test_history_page(self):
        requests_limit = 10
        #requests done by test
        request_path_done = []
        request_paths = [reverse('home'), reverse('requests')]
        while requests_limit > 0:
            request = random.choice(request_paths)
            request_path_done.append(request)
            requests_limit -= 1
            self.client.get(request)
        response = self.client.get(reverse('requests'))
        sp = BeautifulSoup(response.content)
        requests_table_onpage = [elem.getText() for elem in sp.findAll(
            'td', {'class': 'request-path'})]
        self.assertEqual(request_path_done, requests_table_onpage)


class TestEditView(TestCase):
    fixtures = TEST_FIXTURES

    def setUp(self):
        self.user_info = UserInfo.objects.get(pk=1)

    def test_form_on_page(self):
        self.client.login(username=TEST_USER_LOGIN,
                          password=TEST_USER_PASSWORD)
        response = self.client.get(reverse('edit'))
        self.assertTrue(self.user_info.name in response.content)
        self.assertTrue(self.user_info.surname in response.content)
        self.assertTrue(str(self.user_info.birth_date) in response.content)
        self.assertTrue(self.user_info.contact_email in response.content)
        self.assertTrue(self.user_info.contact_jabber in response.content)
        self.assertTrue(self.user_info.contact_skype in response.content)
        self.assertTrue(self.user_info.contact_phone in response.content)
        self.assertTrue(str(self.user_info.contact_other) in response.content)
        self.assertTrue(str(self.user_info.bio) in response.content)

    def test_edit_wthout_login(self):
        self.client.logout()
        response = self.client.get(reverse('edit'))
        self.assertRedirects(
            response,
            reverse('login') + '?next=' + reverse('edit'))

    def test_edit_post_invaliddata(self):
        self.client.login(username=TEST_USER_LOGIN,
                          password=TEST_USER_PASSWORD)
        #not valid data
        response = self.client.post(reverse('edit'),
                                    {'name': 'test',
                                     'surname': 'test',
                                     'birth_date': '100',
                                     'contact_email': 'test@example.com',
                                     'contact_jabber': 'test@jabber.com',
                                     'contact_skype': 'example',
                                     'contact_phone': '123123123',
                                     'contact_other': 'aexample icq',
                                     'bio': 'example bio'})
        user = UserInfo.objects.get(pk=1)
        self.assertNotEqual(user.name, 'test')
        self.assertNotEqual(user.surname, 'test')
        self.assertNotEqual(str(user.birth_date), '100')
        self.assertNotEqual(user.contact_email, 'test@example.com')
        self.assertNotEqual(user.contact_jabber, 'test@jabber.com')
        self.assertNotEqual(user.contact_skype, 'example')
        self.assertNotEqual(user.contact_phone, '123123123')
        self.assertNotEqual(str(user.bio), 'example bio')
        self.client.logout()

    def test_edit_post_validdata(self):
        self.client.login(username=TEST_USER_LOGIN,
                          password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('edit'),
                                    {'name': 'test',
                                     'surname': 'test',
                                     'birth_date': '1990-01-01',
                                     'contact_email': 'test@example.com',
                                     'contact_jabber': 'test@jabber.com',
                                     'contact_skype': 'example',
                                     'contact_phone': '123123123',
                                     'contact_other': 'aexample icq',
                                     'bio': 'example bio'})
        edit_user = UserInfo.objects.get(pk=1)
        self.assertEqual(response.content, '')
        self.assertEqual(edit_user.name, 'test')
        self.assertEqual(edit_user.surname, 'test')
        self.assertEqual(str(edit_user.birth_date), '1990-01-01')
        self.assertEqual(edit_user.contact_email, 'test@example.com')
        self.assertEqual(edit_user.contact_jabber, 'test@jabber.com')
        self.assertEqual(edit_user.contact_skype, 'example')
        self.assertEqual(edit_user.contact_phone, '123123123')
        self.assertEqual(str(edit_user.bio), 'example bio')
