# Generated by Django 5.1.3 on 2025-03-27 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0016_category_alter_courses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на YouTube'),
        ),
    ]
