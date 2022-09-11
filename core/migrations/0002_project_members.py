# Generated by Django 4.1.1 on 2022-09-11 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="members",
            field=models.ManyToManyField(
                related_name="projects_member", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
