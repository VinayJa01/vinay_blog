# Generated by Django 4.2.6 on 2023-11-19 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_userresume_user_resume'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSkill',
        ),
    ]
