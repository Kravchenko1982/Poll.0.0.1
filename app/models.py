# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Person(models.Model):
    fio = models.CharField(max_length=255,verbose_name='ФИО')
    foto = models.ImageField(upload_to='static/foto',verbose_name='Фото')
    age = models.IntegerField(verbose_name='Возраст')


class Polls(models.Model):
    name = models.CharField(max_length=255,verbose_name='наименование')
    startdate = models.DateField(auto_now=False,verbose_name='Дата начала')
    enddate = models.DateField(auto_now=False,verbose_name='Дата окончания')
    max_count = models.IntegerField(verbose_name='Максимальное количество голосов')
    person = models.ManyToManyField(Person,through='PollPerson',related_name='person')
    #close = models.BooleanField()

    def save(self, *args, **kwargs):
        try:
            poll = Polls.objects.get(pk=self.pk)
        except:
            super().save(*args, **kwargs)
            person = Person.objects.all()
            poll = Polls.objects.get(pk=self.pk)
            for pers in person:
                pp = PollPerson(polls=poll,person=pers)
                pp.save()


class PollPerson(models.Model):
    polls = models.ForeignKey(Polls,on_delete='PROTECT',verbose_name='',related_name='poll')
    person = models.ForeignKey(Person,on_delete='PROTECT',verbose_name='',related_name='pers')
    now_count = models.IntegerField(verbose_name='',default=0)

    class Meta:
        ordering = ['-now_count']