# Generated by Django 3.1.7 on 2021-04-07 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20210407_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscribe_confirmed',
        ),
        migrations.AddField(
            model_name='user',
            name='subscribe',
            field=models.BooleanField(default=False, help_text='This will enlist you to newsletter feature. You will get emails on latest news updates. To stop getting emails please set this field false'),
        ),
    ]