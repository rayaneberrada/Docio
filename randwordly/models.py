# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Antonyme(models.Model):
    ant_reference = models.ForeignKey('Mot', models.DO_NOTHING, db_column='ant_reference', related_name='ant_reference')
    antonyme = models.ForeignKey('Mot', models.DO_NOTHING, db_column='antonyme', related_name='antonyme')

    class Meta:
        db_table = 'antonyme'


class Definition(models.Model):
    description = models.CharField(max_length=2000)
    mot = models.ForeignKey('Mot', models.DO_NOTHING)
    exemple = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'definition'


class ListeApprentissage(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    nom = models.CharField(max_length=30)
    mot = models.ForeignKey('Mot', models.DO_NOTHING)

    class Meta:
        db_table = 'liste_apprentissage'


class Mot(models.Model):
    orthographe = models.CharField(max_length=300)
    nature_grammaticale = models.CharField(max_length=255)
    genre = models.CharField(max_length=10, blank=True, null=True)
    etymologie = models.CharField(max_length=5000)

    def __str__(self):
        return self.orthographe

    class Meta:
        db_table = 'mot'


class Note(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    mot = models.ForeignKey(Mot, models.DO_NOTHING)
    note = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        db_table = 'note'


class Reponse(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', models.DO_NOTHING)
    definition = models.ForeignKey(Definition, models.DO_NOTHING)
    reponse = models.IntegerField()
    date = models.DateTimeField()
    taux_validation = models.IntegerField()

    class Meta:
        db_table = 'reponse'


class Synonyme(models.Model):
    syn_reference = models.ForeignKey(Mot, models.DO_NOTHING, db_column='syn_reference', related_name='syn_reference')
    syonyme = models.ForeignKey(Mot, models.DO_NOTHING, db_column='syonyme', related_name='synonyme')

    class Meta:
        db_table = 'synonyme'


class TermeDefinition(models.Model):
    definition = models.ForeignKey(Definition, models.DO_NOTHING)
    terme = models.ForeignKey('UniteTerminologique', models.DO_NOTHING)

    class Meta:
        db_table = 'terme_definition'


class UniteTerminologique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'unite_terminologique'


class Utilisateur(models.Model):
    nom = models.CharField(max_length=20)
    mail = models.CharField(max_length=40)
    mot_de_passe = models.CharField(max_length=40)
    date_inscription = models.DateTimeField()

    class Meta:
        db_table = 'utilisateur'
