# Generated by Django 4.1.3 on 2022-11-26 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_roles_remove_usuario_rol_usuario_id_rol_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
