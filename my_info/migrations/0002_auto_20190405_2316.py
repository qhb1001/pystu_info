# Generated by Django 2.1.3 on 2019-04-05 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=200, verbose_name='配置 key')),
                ('value', models.CharField(max_length=200, verbose_name='配置值')),
                ('remarks', models.CharField(max_length=200, verbose_name='备注')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='log_ip',
            field=models.CharField(default=None, max_length=200, verbose_name='登陆IP'),
        ),
    ]
