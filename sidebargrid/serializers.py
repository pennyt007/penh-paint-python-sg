from rest_framework import serializers
from . import models


class SidebarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sidebar
        fields = ['sidebar_id', 'name']


class SidebarCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SidebarCarousel
        fields = ['properties']


class SidebarButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SidebarButton
        fields = ['properties']


class GridSerializer(serializers.ModelSerializer):
    filtered = serializers.SerializerMethodField()
    unfiltered = serializers.SerializerMethodField()

    class Meta:
        model = models.Grid
        fields = ['data', 'data_key', 'columns', 'filtered', 'unfiltered']

    def get_filtered(self, Grid):
        return {}

    def get_unfiltered(self, Grid):
        return {}


class GridSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Grid
        fields = ['data']


class GridFilterFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GridFilterField
        fields = ['grid_filter_field_id','name', 'data_field', 'values']


class GridFilterSerializer(serializers.ModelSerializer):
    current_filter = serializers.SerializerMethodField()
    number_checked = serializers.SerializerMethodField()
    grid_filter_field = GridFilterFieldSerializer(read_only=True)

    class Meta:
        model = models.GridFilter
        fields = ['grid_filter_id', 'current_filter',
                  'number_checked', 'grid_filter_field']

    def get_current_filter(self, GridFilter):
        return []

    def get_number_checked(self, GridFilter):
        return 0


class SidebarItemSerializer(serializers.ModelSerializer):
    sidebar = SidebarSerializer(read_only=True)
    grid = GridSerializer(read_only=True)

    class Meta:
        model = models.SidebarItem
        fields = ['is_parent_item', 'parent_item_id', 'name',
                  'icon', 'is_selected', 'order', 'sidebar', 'grid']


class SidebarItemWithGridFiltersSerializer(serializers.ModelSerializer):
    sidebar = SidebarSerializer(read_only=True)
    grid = GridSerializer(read_only=True)
    grid_filters = serializers.SerializerMethodField()

    class Meta:
        model = models.SidebarItem
        fields = ['sidebar', 'grid', 'grid_filters']

    def get_grid_filters(self, obj):
        # Access prefetched related GridFilter objects
        return GridFilterSerializer(obj.grid.prefetched_grid_filters, many=True).data \
            if hasattr(obj.grid, 'prefetched_grid_filters') else []


class SidebarItemTreeSerializer(serializers.ModelSerializer):
    grid = GridSimpleSerializer(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.SidebarItem
        fields = ['sidebar_item_id', 'name', 'icon', 'is_selected',
                  'order', 'is_parent_item', 'parent_item_id', 'grid', 'children']

    def get_children(self, obj):
        # children = obj.children.all()
        return SidebarItemTreeSerializer(obj.prefetched_children, many=True).data\
            if hasattr(obj, 'prefetched_children') else []
