from django.test import TestCase
from django.template import Context
from django.template import Template
from django.db.models import get_app
from django.db.models import get_models
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.management.base import ImproperlyConfigured
from models import UserInfo
from models import RequestHistoryEntry
from models import ModelHistoryEntry
from models import RequestPriorityEntry
from management.commands import appmodels
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import random
import re


TEST_LOGIN_USERNAME = 'admin'
TEST_LOGIN_PASSWORD = 'admin'
TEST_FIXTURES = ['db_data.json']


class TestIndexView(TestCase):
    fixtures = TEST_FIXTURES

    def setUp(self):
        self.user = UserInfo.objects.get(pk=1)

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        for user_attr in self.user.attrDict().values():
            self.assertIn(str(user_attr), response.content)


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
        requests_table_onpage = [elem.getText() for elem in sp.findAll(
            'td', {'class': re.compile('request-path.*')})]
        self.assertEqual(request_path_done, requests_table_onpage)


class TestEditView(TestCase):
    fixtures = TEST_FIXTURES

    def setUp(self):
        self.user_info = UserInfo.objects.get(pk=1)
        self.new_attrs_invalid = {
            'name': 'test',
            'surname': 'test',
            'birth_date': '100',
            'contact_email': '',
            'contact_jabber': 'test@jabber.com',
            'contact_skype': 'example',
            'contact_phone': '123123123',
            'contact_other': 'aexample icq',
            'bio': 'example bio'}
        self.new_attrs_valid = self.new_attrs_invalid.copy()
        self.new_attrs_valid['birth_date'] = '1990-01-01'
        self.new_attrs_valid['contact_email'] = 'test@example.com'

    def test_form_on_page(self):
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.get(reverse('edit'))
        for user_attr in self.user_info.attrDict().values():
            self.assertIn(str(user_attr), response.content)

    def test_edit_wthout_login(self):
        self.client.logout()
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('login') + '?next=' + reverse('edit'))

    def test_edit_custom_widget(self):
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.get(reverse('edit'))
        self.assertIn("('#id_birth_date').datepicker", response.content)

    def test_edit_post_invaliddata(self):
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.post(reverse('edit'), self.new_attrs_invalid)
        #errors are on page?
        sp = BeautifulSoup(response.content)
        error_list = sp.findAll('ul', {'class': 'errorlist'})
        user = UserInfo.objects.get(pk=1)
        self.assertIn('Enter a valid date.', error_list[0].getText())
        self.assertIn('This field is required.', error_list[1].getText())
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('This field is required.', response.content)
        for key, val in self.new_attrs_invalid.items():
            self.assertNotEqual(user.attrDict()[key], val)
        self.client.logout()

    def test_edit_post_validdata(self):
        #valid data
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        self.client.post(reverse('edit'), self.new_attrs_valid)
        edited_user = UserInfo.objects.get(pk=1)
        #user changed
        for key, val in self.new_attrs_valid.items():
            self.assertEqual(val, edited_user.attrDict()[key])
        self.client.logout()

    def test_edit_ajax_validdata(self):
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.post(reverse('edit_ajax'),
                                    self.new_attrs_valid,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('request_result', response.content)
        self.assertIn('Successfuly saved.', response.content)
        edited_user = UserInfo.objects.get(pk=1)
        #user changed
        for key, val in self.new_attrs_valid.items():
            self.assertEqual(val, edited_user.attrDict()[key])

    def test_edit_ajax_invaliddata(self):
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.post(reverse('edit_ajax'),
                                    self.new_attrs_invalid,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('request_result', response.content)
        self.assertIn('Error occurred', response.content)
        edited_user = UserInfo.objects.get(pk=1)
        #user not changed
        for key, val in self.new_attrs_invalid.items():
            self.assertNotEqual(val, edited_user.attrDict()[key])


class TestAdminLinkTag(TestCase):
    fixtures = TEST_FIXTURES

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
    fixtures = TEST_FIXTURES

    def setUp(self):
        self.app = 'pyta'
        self.in_app = get_app(self.app)
        self.not_exists_app = 'i_am_app'
        self.models = get_models(self.in_app)

    def command_call(args, app_name=''):
        args = [app_name]
        opts = {}
        err = StringIO()
        out = StringIO()
        call_command('appmodels',stdout=out, stderr=err, *args, **opts)
        err.seek(0), out.seek(0)
        std_out = out.read()
        std_err = err.read()
        return std_out, std_err

    def test_model_displaying(self):
        std_out, std_err = self.command_call(self.app)
        self.assertEqual(len(std_out.splitlines()),
                         len(std_err.splitlines()))

    def test_nonexists_app(self):
        self.assertRaises(self.command_call(self.not_exists_app),
                          CommandError)




class TestSignalRecivier(TestCase):
    fixtures = TEST_FIXTURES

    def setUp(self):
        self.model = UserInfo.objects.get(pk=1)
        self.created_model = RequestHistoryEntry.objects.create(
            request_path="/somepath",
            request_method="POST")

    def test_creation_signal(self):
        creation_history_entry = ModelHistoryEntry.objects.latest(
            'change_time')
        self.assertEqual(creation_history_entry.model_name,
                         self.created_model.__class__.__name__)
        self.assertIn(
            "CREATED",
            creation_history_entry.__unicode__())

    def test_modify_signal(self):
        self.model.name = "Test"
        self.model.save()
        modify_history_entry = ModelHistoryEntry.objects.latest('change_time')
        self.assertEqual(modify_history_entry.model_name,
                         self.model.__class__.__name__)
        self.assertIn("MODIFIED", modify_history_entry.__unicode__())

    def test_delete_signal(self):
        model_name = self.model.__class__.__name__
        self.model.delete()
        delete_history_entry = ModelHistoryEntry.objects.latest('change_time')
        self.assertEqual(delete_history_entry.model_name, model_name)
        self.assertIn("DELETED", delete_history_entry.__unicode__())


class TestChangeRequestPriority(TestCase):
    fixtures = TEST_FIXTURES

    def test_ajax_edition_priority_valid(self):
        ''' Test for valid data submission'''
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.post(
            reverse('edit_request_priority'),
            {'request_path': reverse('home'), 'request_priority': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        priority_entry = RequestPriorityEntry.objects.get(pk=1)
        self.client.get(reverse('home'))
        request_entry = RequestHistoryEntry.objects.get(
            request_path=reverse('home'))
        self.assertIn('success', response.content)
        self.assertEqual(priority_entry.request_priority,
                         request_entry.request_priority)

    def test_ajax_edition_priority_invalid(self):
        ''' Test for invalid data submission'''
        self.client.login(username=TEST_LOGIN_USERNAME,
                          password=TEST_LOGIN_PASSWORD)
        response = self.client.post(
            reverse('edit_request_priority'),
            {'request_path': reverse('home'), 'request_priority': 'a'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('Error', response.content)
