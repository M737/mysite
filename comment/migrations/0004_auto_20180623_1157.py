# Generated by Django 2.0.4 on 2018-06-23 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root_comment', to='comment.Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_comment', to='comment.Message'),
        ),
    ]
