# Generated by Django 4.1.3 on 2022-11-26 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usuario_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='rol',
        ),
        migrations.AddField(
            model_name='usuario',
            name='id_rol_fk',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='users.roles'),
        ),
    ]