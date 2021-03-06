# Generated by Django 2.2.4 on 2022-06-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('date_hired', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete='cascade', related_name='item', to='belt_app.User')),
                ('users', models.ManyToManyField(related_name='wishlist', to='belt_app.User')),
            ],
        ),
    ]
