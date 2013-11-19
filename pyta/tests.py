from django.test import TestCase
from django.template import Context
from django.template import Template
from django.db.models import get_app
from django.db.models import get_models
from django.core.urlresolvers import reverse
from models import UserInfo
from models import RequestHistoryEntry
from BeautifulSoup import BeautifulSoup
import random
import os
import subprocess
import datetime


class TestIndexView(TestCase):
    fixtures = ['db_data.json']

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
        #this is requests done by test
        request_path_done = []
        request_paths = [reverse('home'), reverse('requests')]
        while requests_limit > 0:
            request = random.choice(request_paths)
            request_path_done.append(request)
            requests_limit -= 1
            self.client.get(request)
        response = self.client.get(reverse('requests'))
        sp = BeautifulSoup(response.content)
        requests_table_onpage = [elem.getText() for elem in sp.findAll
                                 ('td', {'class': 'request-path'})]
        self.assertEqual(request_path_done, requests_table_onpage)


class TestEditView(TestCase):
    fixtures = ['db_data.json']

    def setUp(self):
        self.user_info = UserInfo.objects.get(pk=1)

    def test_form_on_page(self):
        self.client.login(username='admin', password='admin')
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
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('login') + '?next=' + reverse('edit'))

    def test_edit_custom_widget(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit'))
        self.assertIn("('#id_birth_date').datepicker", response.content)

    def test_edit_post_invaliddata(self):
        self.client.login(username='admin', password='admin')
        #not valid data
        response = self.client.post(reverse('edit'),
                                    {'name': 'test',
                                     'surname': 'test',
                                     'birth_date': '100',
                                     'contact_email': '',
                                     'contact_jabber': 'test@jabber.com',
                                     'contact_skype': 'example',
                                     'contact_phone': '123123123',
                                     'contact_other': 'aexample icq',
                                     'bio': 'example bio'})
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('This field is required.', response.content)
        #errors are on page?
        sp = BeautifulSoup(response.content)
        error_list = sp.findAll('ul', {'class': 'errorlist'})
        self.assertIn('Enter a valid date.', error_list[0].getText())
        self.assertIn('This field is required.', error_list[1].getText())
        #user not changed
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
        #valid data
        self.client.login(username='admin', password='admin')
        self.client.post(reverse('edit'),
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
        #user changed
        self.assertEqual(edit_user.name, 'test')
        self.assertEqual(edit_user.surname, 'test')
        self.assertEqual(str(edit_user.birth_date), '1990-01-01')
        self.assertEqual(edit_user.contact_email, 'test@example.com')
        self.assertEqual(edit_user.contact_jabber, 'test@jabber.com')
        self.assertEqual(edit_user.contact_skype, 'example')
        self.assertEqual(edit_user.contact_phone, '123123123')
        self.assertEqual(str(edit_user.bio), 'example bio')
        self.client.logout()

    def test_edit_ajax_validdata(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('edit_ajax'),
                                    {'name': 'test',
                                     'surname': 'test',
                                     'birth_date': '1990-01-01',
                                     'contact_email': 'test@example.com',
                                     'contact_jabber': 'test@jabber.com',
                                     'contact_skype': 'example',
                                     'contact_phone': '123123123',
                                     'contact_other': 'example icq',
                                     'bio': 'example bio'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('request_result', response.content)
        self.assertIn('Successfuly saved.', response.content)
        userinfo = UserInfo.objects.get(pk=1)
        #user changed
        self.assertEqual(userinfo.name, u'test')
        self.assertEqual(userinfo.surname, 'test')
        self.assertEqual(str(userinfo.birth_date), '1990-01-01')
        self.assertEqual(userinfo.contact_email, 'test@example.com')
        self.assertEqual(userinfo.contact_jabber, 'test@jabber.com')
        self.assertEqual(userinfo.contact_skype, 'example')
        self.assertEqual(userinfo.contact_phone, '123123123')
        self.assertEqual(str(userinfo.bio), 'example bio')

    def test_edit_ajax_invaliddata(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('edit_ajax'),
                                    {'name': 'test',
                                     'surname': 'test',
                                     'birth_date': '1111',
                                     'contact_email': 'test@example.com',
                                     'contact_jabber': 'test@jabber.com',
                                     'contact_skype': 'example',
                                     'contact_phone': '123123123',
                                     'contact_other': 'example icq',
                                     'bio': 'example bio'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('request_result', response.content)
        self.assertIn('Error', response.content)
        self.assertIn
        userinfo = UserInfo.objects.get(pk=1)
        #user not changed
        self.assertNotEqual(userinfo.name, u'test')
        self.assertNotEqual(userinfo.surname, 'test')
        self.assertNotEqual(str(userinfo.birth_date), '1990-01-01')
        self.assertNotEqual(userinfo.contact_email, 'test@example.com')
        self.assertNotEqual(userinfo.contact_jabber, 'test@jabber.com')
        self.assertNotEqual(userinfo.contact_skype, 'example')
        self.assertNotEqual(userinfo.contact_phone, '123123123')
        self.assertNotEqual(str(userinfo.bio), 'example bio')


class TestAdminLinkTag(TestCase):
    fixtures = ['db_data.json']

    def setUp(self):
        self.user_model = UserInfo.objects.get(pk=1)
        self.client.get(reverse('home'))
        self.history_entry = RequestHistoryEntry.objects.get(pk=1)
        self.context = Context({'user_info': self.user_model,
                                'history_entry': self.history_entry})
        self.not_rendered = Template(
            '''{% load pyta_extras %}
            {% get_admin_link user_info %}
            {% get_admin_link history_entry %}''')
        self.rendered = self.not_rendered.render(self.context)

    def test_link_rendering(self):
        self.assertIn('/pyta/userinfo/1/', self.rendered)
        self.assertIn('/pyta/requesthistoryentry/1/', self.rendered)
        self.assertEqual('', self.not_rendered.render(Context()).strip())
        self.assertEqual('',
                         self.not_rendered.render(
                             Context({"user_info": 1})).strip()
                         )

    def test_link_displayng(self):
        response = self.client.get(reverse('home'))
        self.assertIn(self.rendered.strip().split()[0], response.content)


class TestModelDisplaying(TestCase):
    fixtures = ['db_data.json']

    def setUp(self):
        self.app = 'pyta'
        self.in_app = get_app(self.app)
        self.not_exists_app = 'i_am_app'
        self.models = get_models(self.in_app)

    def test_displaing(self):
        result = subprocess.Popen(['python manage.py appmodels %s' % self.app],
                                  shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        result_stdout = result.stdout.read()
        result_stderr = result.stderr.read()
        self.assertEqual(len(result_stdout.splitlines()),
                         len(result_stderr.splitlines()))
        for model in self.models:
            self.assertIn(model.__name__, result_stdout)
            self.assertIn("error:\tMODEL " + model.__name__, result_stderr)

    def test_invalid_app_name(self):
        result = subprocess.Popen(['python manage.py appmodels %s' %
                                  self.not_exists_app],
                                  shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        result_err = result.stderr.read()
        self.assertIn('could not be found', result_err)

    def test_invalid_args(self):
        result = subprocess.Popen(['python manage.py appmodels'],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        result_err = result.stderr.read()
        self.assertIn('needs 1 argument', result_err)


class TestShellScript(TestCase):
    def setUp(self):
        self.app = 'pyta'
        self.in_app = get_app(self.app)
        self.script_name = 'appmodels.sh'

    def test_created_file(self):
        result = subprocess.Popen(['bash %s' % self.script_name],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        result_stderr = result.stderr.read()
        result_stdout = result.stdout.read()
        filename = str(datetime.date.today().strftime('%Y%m%d')) + '.dat'
        data = open(filename, 'r').read()
        self.assertEqual(0, len(result_stderr.splitlines()))
        #duplicated and written to file?
        self.assertEqual(
            len(result_stdout.splitlines()), len(data.splitlines()))
        os.remove(filename)
