# Generated by Django 2.2b1 on 2019-03-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ActivityModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='test')),
            ],
        ),
    ]