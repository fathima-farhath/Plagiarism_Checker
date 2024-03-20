# Generated by Django 4.1.7 on 2024-03-19 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('class', '0004_workspace_student'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='membership',
            name='is_join',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspace', to='class.workspace'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='profiles.student'),
        ),
        migrations.RemoveField(
            model_name='membership',
            name='workspace',
        ),
    ]
