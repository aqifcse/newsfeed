# Generated by Django 3.1.7 on 2021-04-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20210407_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subscribe_confirmed',
            field=models.BooleanField(default=False, help_text='This will enlist you to newsletter feature. You will get emails on latest news updates'),
        ),
    ]
