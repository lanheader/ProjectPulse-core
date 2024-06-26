# Generated by Django 4.1.13 on 2024-03-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apps", "0006_alter_projectrolesusers_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="resource_type",
            field=models.IntegerField(
                choices=[(1, "服务器"), (2, "数据库"), (3, "VPN")],
                default="1",
                verbose_name="资源类型",
            ),
        ),
    ]
