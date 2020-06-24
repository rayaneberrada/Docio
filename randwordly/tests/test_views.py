import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from randwordly.models import Mot, ListeApprentissage

class TestIndex(TestCase):
    """docstring for TestIndex"""
    @classmethod
    def setUpTestData(cls):
        cls.Mot = Mot.objects.create(
            orthographe="test",
            nature_grammaticale = "verbe",
            genre = "m",
            etymologie="Inconnue"
            )
        user = User.objects.create(username='test', email='test@test.com', is_active=True)
        user.set_password('Test1234')
        user.save()

    def test_view_accessible(self):
        self.login = self.client.login(username='test', password='Test1234')
        response = self.client.get(reverse('randwordly:random'))
        context = list(response.context)[:-1][0]
        self.assertEqual(response.status_code, 200)
        self.assertTrue('listes' in context)
        self.assertEqual(len(context['listes']), 1)

    def test_view_post_context(self):
        response = self.client.post(reverse('randwordly:random'))
        response = json.loads(response.content)
        self.assertTrue('word' in response)
        self.assertEqual(len(response['definitions']), 4)


class testAddToListe(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
        self.user.set_password('Test1234')
        self.user.save()
        word = Mot.objects.create(
            orthographe="test",
            nature_grammaticale = "verbe",
            genre = "m",
            etymologie="Inconnue"
            )
        word.save()
        test_word = Mot.objects.create(
            orthographe="test2",
            nature_grammaticale = "verbe",
            genre = "m",
            etymologie="Inconnue"
            ).save()
        ListeApprentissage.objects.create(
            utilisateur=self.user,
            nom="test",
            mot=word
            ).save()

    def test_add_word_to_list(self):
        liste = ListeApprentissage.objects.filter(utilisateur=self.user)
        self.assertEqual(len(liste), 1)

        datas = {
                'word': 'test2',
                'listes': 'test',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        liste = ListeApprentissage.objects.filter(utilisateur=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(liste), 2)

    def test_fail_to_add(self):
        datas = {
                'word': 'DoesntExistInDB',
                'listes': 'test',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        self.assertEqual(response.status_code, 400)

        datas = {
                'word': 'test2',
                'listes': 'DoesntExistInDB',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        self.assertEqual(response.status_code, 400)
