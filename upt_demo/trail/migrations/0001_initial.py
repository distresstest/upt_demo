# Generated by Django 3.0.5 on 2020-05-01 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.CharField(default='NO_ACTION', max_length=30)),
                ('action_verb', models.CharField(choices=[('TAKE', 'Take Item'), ('USE', 'Use Item')], default='1', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='Item', max_length=40)),
                ('item_description', models.TextField(default='This is an item', max_length=200)),
                ('item_alt', models.CharField(default='This is an item', max_length=40)),
                ('item_image', models.ImageField(blank=True, upload_to='location_images')),
            ],
        ),
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trail_name', models.CharField(max_length=120)),
                ('trail_description', models.TextField(blank=True, null=True)),
                ('trail_mission', models.CharField(default='This is a mission', max_length=75)),
                ('trail_total_items', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=120)),
                ('location_description', models.TextField(blank=True, null=True)),
                ('location_url', models.CharField(default='This is a URL', max_length=16)),
                ('location_inventory', models.ManyToManyField(blank=True, to='trail.Item')),
                ('location_visit_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=120)),
                ('game_mission', models.TextField(blank=True, null=True)),
                ('game_url', models.CharField(max_length=16)),
                ('game_start', models.DateTimeField(auto_now_add=True)),
                ('game_total_items', models.IntegerField(default=0)),
                ('game_duration', models.DurationField(null=True)),
                ('game_progress', models.IntegerField(default=0)),
                ('game_status', models.CharField(default='Not Started', max_length=20)),
                ('game_event_list', models.ManyToManyField(blank=True, to='trail.Event')),
                ('game_inventory', models.ManyToManyField(blank=True, to='trail.Item')),
                ('game_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('game_trail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Trail')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_trail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Trail'),
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context_index', models.IntegerField(default=0)),
                ('context_text', models.TextField(blank=True, null=True)),
                ('context_action', models.ManyToManyField(blank=True, to='trail.Action')),
                ('context_enable_events', models.ManyToManyField(blank=True, to='trail.Event')),
                ('context_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Location')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='action_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Event'),
        ),
        migrations.AddField(
            model_name='action',
            name='action_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trail.Item'),
        ),
    ]
