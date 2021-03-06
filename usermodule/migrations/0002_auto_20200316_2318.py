# Generated by Django 3.0.3 on 2020-03-16 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermodule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post1',
            name='pcount',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermodule.Post1')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermodule.User')),
            ],
        ),
    ]
