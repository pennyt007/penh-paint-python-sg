from django.db import models


class Sidebar(models.Model):
    sidebar_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class SidebarButton(models.Model):
    sidebar_button_id = models.IntegerField(primary_key=True)
    sidebar = models.ForeignKey('Sidebar', models.CASCADE)
    properties = models.JSONField()


class SidebarCarousel(models.Model):
    sidebar_carousel_id = models.AutoField(primary_key=True)
    sidebar = models.ForeignKey('Sidebar', models.CASCADE)
    properties = models.JSONField()


class Grid(models.Model):
    grid_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    data = models.CharField(max_length=50, blank=True, null=True)
    data_filtered = models.CharField(max_length=50, blank=True, null=True)
    data_key = models.CharField(max_length=50, blank=True, null=True)
    columns = models.JSONField(blank=True, null=True)


# class SidebarItem(models.Model):
#     sidebar_item_id = models.AutoField(primary_key=True)
#     sidebar = models.ForeignKey('Sidebar', models.CASCADE)
#     grid = models.ForeignKey('Grid', models.PROTECT)
#     is_parent_item = models.IntegerField()
#     parent_item_id = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=50)
#     icon = models.CharField(max_length=50, blank=True, null=True)
#     is_selected = models.IntegerField()
#     order = models.IntegerField()
    
class SidebarItem(models.Model):
    sidebar_item_id = models.AutoField(primary_key=True)
    sidebar = models.ForeignKey('Sidebar', models.CASCADE)
    grid = models.ForeignKey('Grid', models.PROTECT)
    is_parent_item = models.BooleanField(default=False)
    parent_item = models.ForeignKey('self', models.CASCADE, related_name='children', null=True, blank=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_selected = models.BooleanField(default=False)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def get_tree(self):
        """
        Recursively build a tree structure starting from the current instance.
        """
        tree = {
            'id': self.sidebar_item_id,
            'name': self.name,
            'icon': self.icon,
            'is_selected': self.is_selected,
            'order': self.order,
            'children': []
        }
        # Recursively add children
        for child in self.children.all():
            tree['children'].append(child.get_tree())
        return tree  


class GridFilterField(models.Model):
    grid_filter_field_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    data_field = models.CharField(max_length=50)
    values = models.JSONField()


class GridFilter(models.Model):
    grid_filter_id = models.AutoField(primary_key=True)
    grid = models.ForeignKey('Grid', models.CASCADE)
    grid_filter_field = models.ForeignKey(GridFilterField, models.CASCADE)
