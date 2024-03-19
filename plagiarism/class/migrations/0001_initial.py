# Generated by Django 5.0.3 on 2024-03-19 07:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WorkSpace',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('stream', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=8, null=True)),
                ('details', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]