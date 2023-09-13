# Generated by Django 4.2.3 on 2023-07-11 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('duration', models.PositiveIntegerField()),
                ('age_limit', models.PositiveIntegerField()),
                ('audience_count', models.PositiveIntegerField()),
                ('production_company', models.CharField(max_length=100)),
                ('release_year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(choices=[('감독', '감독'), ('주연', '주연'), ('조연', '조연')], max_length=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.participant')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='participants',
            field=models.ManyToManyField(through='movies.Role', to='movies.participant'),
        ),
    ]