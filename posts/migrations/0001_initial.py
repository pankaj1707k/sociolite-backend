# Generated by Django 4.0.5 on 2022-07-10 11:21

from django.db import migrations, models
import posts.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='text')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'like',
                'verbose_name_plural': 'likes',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('image', models.ImageField(blank=True, null=True, upload_to=posts.utils.get_post_image_path, verbose_name='image')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-updated_on'],
            },
        ),
    ]
