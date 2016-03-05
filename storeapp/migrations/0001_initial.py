# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 13:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iban', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('url', models.URLField(unique=True)),
                ('price', models.FloatField()),
                ('sold', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('genre', models.CharField(choices=[('Action/Adventure', 'Action/Adventure'), ('RPG', 'RPG'), ('Shooter', 'Shooter'), ('Puzzle', 'Puzzle')], default='Shooter', max_length=50)),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='storeapp.Developer')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.ManyToManyField(to='storeapp.Game')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SavedGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_data', models.TextField(default='')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storeapp.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_games', to='storeapp.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='storeapp.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='storeapp.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storeapp.Game')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='storeapp.Player')),
            ],
        ),
    ]
