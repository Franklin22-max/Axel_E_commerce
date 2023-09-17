# Generated by Django 4.2.5 on 2023-09-16 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_user_gender_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default=('O', 'Others'), max_length=7),
        ),
    ]
