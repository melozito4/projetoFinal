# Generated by Django 5.2.1 on 2025-06-05 17:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_profile_tipo_utilizador'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InscricaoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('instituicao', models.CharField(blank=True, max_length=150)),
                ('cargo', models.CharField(blank=True, max_length=100)),
                ('tipo_registo', models.CharField(max_length=50)),
                ('nif', models.CharField(blank=True, max_length=20)),
                ('morada', models.TextField(blank=True)),
                ('data_inscricao', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
