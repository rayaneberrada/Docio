import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from randwordly.models import Mot, ListeApprentissage, MotListe

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
            id= 1,
            orthographe="test",
            nature_grammaticale = "verbe",
            genre = "m",
            etymologie="Inconnue"
            )
        word.save()
        ListeApprentissage.objects.create(
            id= 1,
            utilisateur=self.user,
            nom="test",
            ).save()
        MotListe.objects.create(
            mot_id = 1,
            liste_id = 1
            )

    def test_add_word_to_list(self):
        self.login = self.client.login(username='test', password='Test1234')
        liste = ListeApprentissage.objects.filter(utilisateur=self.user)
        self.assertEqual(len(liste), 1)

        datas = {
                'word_id': 1,
                'listes': 'test',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        liste = MotListe.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(liste.mot_id, 1)
        self.assertEqual(liste.liste_id, 1)

    def test_fail_to_add(self):
        self.login = self.client.login(username='test', password='Test1234')
        datas = {
                'word_id': 100,
                'listes': 'test',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        self.assertEqual(response.status_code, 400)

        datas = {
                'word_id': 2,
                'listes': 'DoesntExistInDB',
                }
        response = self.client.post(reverse('randwordly:add_favorite'), datas)
        self.assertEqual(response.status_code, 400)

class testCreateList(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(username='test', email='test@test.com', is_active=True)
        self.user.set_password('Test1234')
        self.user.save()
        word = Mot.objects.create(
        	id = 3,
            orthographe = "test",
            nature_grammaticale = "verbe",
            genre = "m",
            etymologie="Inconnue"
            )
        word.save()

        liste = ListeApprentissage.objects.create(
            utilisateur=self.user,
            nom = "existing_liste",
            )
        liste.save()

        list_word = MotListe.objects.create(
            mot_id = word.id,
            liste_id = liste.id
            )
        list_word.save()

    def test_success_to_create(self):
        self.login = self.client.login(username='test', password='Test1234')
        datas = {
                'new_list_name': 'list_to_create',
                'list_chosen': ['existing_liste'],
                }
        response = self.client.post(reverse('randwordly:liste'), datas)
        liste = ListeApprentissage.objects.get(nom='list_to_create')
        check_liste_create = ListeApprentissage.objects.get(nom='list_to_create')
        check_word_added = MotListe.objects.filter(liste_id=check_liste_create.id)
        self.assertTrue(check_liste_create)
        self.assertEqual(check_word_added[0].mot_id, 3)
        self.assertEqual(response.status_code, 200)