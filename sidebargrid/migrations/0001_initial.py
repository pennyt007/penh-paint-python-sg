# Generated by Django 5.0.3 on 2024-03-07 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('grid_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('data', models.CharField(blank=True, max_length=50, null=True)),
                ('data_filtered', models.CharField(blank=True, max_length=50, null=True)),
                ('data_key', models.CharField(blank=True, max_length=50, null=True)),
                ('columns', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GridFilterField',
            fields=[
                ('grid_filter_field_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('data_field', models.CharField(max_length=50)),
                ('values', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('sidebar_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GridFilter',
            fields=[
                ('grid_filter_id', models.AutoField(primary_key=True, serialize=False)),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sidebargrid.grid')),
                ('grid_filter_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sidebargrid.gridfilterfield')),
            ],
        ),
        migrations.CreateModel(
            name='SidebarButton',
            fields=[
                ('sidebar_button_id', models.IntegerField(primary_key=True, serialize=False)),
                ('properties', models.JSONField()),
                ('sidebar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sidebargrid.sidebar')),
            ],
        ),
        migrations.CreateModel(
            name='SideBarCarousel',
            fields=[
                ('sidebar_carousel_id', models.AutoField(primary_key=True, serialize=False)),
                ('properties', models.JSONField()),
                ('sidebar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sidebargrid.sidebar')),
            ],
        ),
        migrations.CreateModel(
            name='SidebarItem',
            fields=[
                ('sidebar_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_parent_item', models.IntegerField()),
                ('parent_item_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(blank=True, max_length=50, null=True)),
                ('is_selected', models.IntegerField()),
                ('order', models.IntegerField()),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sidebargrid.grid')),
                ('sidebar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sidebargrid.sidebar')),
            ],
        ),
    ]
