# Generated by Django 3.0 on 2019-12-11 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='image',
            field=models.FileField(upload_to='images/'),
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wrong_answers_reference_counter', models.IntegerField(default=0)),
                ('wrong_answers_translation_counter', models.IntegerField(default=0)),
                ('correct_answers_reference_counter', models.IntegerField(default=0)),
                ('correct_answers_translation_counter', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('expression', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datasets.Expression')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
