# Generated by Django 4.1.5 on 2023-01-16 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0005_alter_postcomment_post_alter_postlike_post"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="postlike",
            constraint=models.UniqueConstraint(
                fields=("post", "user"), name="post_user_like_unique"
            ),
        ),
    ]
