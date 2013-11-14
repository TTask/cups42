from django.test import TestCase
from models import UserInfo
import views
from django.core.urlresolvers import reverse


class TestIndexView(TestCase):
    
    def setUp(self):
        fixtures = ['initial_data.json']
        self.user = UserInfo.objects.get(pk=1)

    def test_index_view(self):
        response = self.client.get(reverse(views.home_view))
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
