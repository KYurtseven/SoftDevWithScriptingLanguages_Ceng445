# Generated by Django 2.1.4 on 2018-12-29 19:51

from django.db import migrations, models
import djongo.models.fields
import question.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_id', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('choices', djongo.models.fields.ArrayModelField(model_container=question.models.Choices)),
                ('topics', djongo.models.fields.ArrayModelField(model_container=question.models.Topics)),
                ('embeds', djongo.models.fields.ArrayModelField(model_container=question.models.Embeds)),
                ('parent', models.CharField(blank=True, max_length=50)),
                ('ask_date', models.DateField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
    ]