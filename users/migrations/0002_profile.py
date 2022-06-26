# Generated by Django 4.0.5 on 2022-06-26 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='location')),
                ('work', models.CharField(blank=True, max_length=200, verbose_name='work')),
                ('about', models.TextField(blank=True, verbose_name='about')),
                ('date_of_birth', models.DateField(blank=True, verbose_name='date of birth')),
                ('picture', models.ImageField(default='profile/default.png', upload_to=users.utils.get_profile_image_path, verbose_name='picture')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]