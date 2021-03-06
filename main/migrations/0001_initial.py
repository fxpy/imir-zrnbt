# Generated by Django 2.1 on 2019-10-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=256, verbose_name='Телефон')),
                ('name', models.CharField(max_length=256, verbose_name='ФИО')),
                ('profession', models.CharField(max_length=256, verbose_name='Профессия')),
                ('geobase', models.CharField(max_length=256, verbose_name='Геобаз')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateTimeField(auto_now_add=True, verbose_name='Первый запуск бота, UTC')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=256, null=True, verbose_name='Логин')),
                ('last_action', models.CharField(blank=True, max_length=256, null=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
    ]
