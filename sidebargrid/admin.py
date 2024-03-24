from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.contrib import admin
from django.urls import reverse
from . import models

@admin.register(models.Sidebar)
class SidebarAdmin(admin.ModelAdmin):
    list_display = ['sidebar_id','name', 'sidebaritem_count']

    @admin.display(ordering='sidebaritem_count')
    def sidebaritem_count(self, sidebar):
        url = (
            reverse('admin:sidebargrid_sidebaritem_changelist')
            + '?'
            + urlencode({'sidebar__sidebar_id': str(sidebar.sidebar_id)})
        )
        return format_html('<a href="{}">{}</a>',url, sidebar.sidebaritem_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            sidebaritem_count = Count('sidebaritem')
        )

@admin.register(models.SidebarButton)
class SidebarButtonAdmin(admin.ModelAdmin):
    list_display = ['sidebar_button_id', 'sidebar_name', 'properties']
    ordering = ['sidebar']
    list_select_related = ['sidebar']

    def sidebar_name(self,sidebarbutton):
        return sidebarbutton.sidebar.name

@admin.register(models.SidebarCarousel)
class SidebarCarouselAdmin(admin.ModelAdmin):
    list_display = ['sidebar_carousel_id','sidebar_name','properties']
    ordering = ['sidebar']
    list_select_related = ['sidebar']

    def sidebar_name(self,sidebarcarousel):
        return sidebarcarousel.sidebar.name


@admin.register(models.SidebarItem)
class SidebarItemAdmin(admin.ModelAdmin):
    list_display = ['sidebar_item_id', 'name', 'sidebar_name', 'grid_name', 'is_parent_item', 'parent_item_id', 'icon', 'is_selected', 'order']
    list_filter = ['sidebar__name']
    list_select_related = ['sidebar','grid']
    ordering = ['sidebar_item_id']
    search_fields = ['sidebar__name__istartswith']
  

    def sidebar_name(self, sidebaritem):
        return sidebaritem.sidebar.name

    def grid_name(self, sidebaritem):
        return sidebaritem.grid.name

@admin.register(models.Grid)
class GridAdmin(admin.ModelAdmin):
    list_display = ['grid_id', 'name', 'data', 'data_filtered', 'data_key', 'columns', 'gridfilter_count']

    @admin.display(ordering='gridfilter_count')
    def gridfilter_count(self, grid):
        url = (
            reverse('admin:sidebargrid_gridfilter_changelist')
            + '?'
            + urlencode({'grid__grid_id': str(grid.grid_id)})
        )
        return format_html('<a href="{}">{}</a>',url, grid.gridfilter_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            gridfilter_count = Count('gridfilter')
        )


@admin.register(models.GridFilterField)
class GridFilterField(admin.ModelAdmin):
    list_display = ['grid_filter_field_id','name','data_field', 'values']

@admin.register(models.GridFilter)
class GridFilter(admin.ModelAdmin):
    list_display = ['grid_filter_id', 'grid_name', 'grid_filter_field_name']
    ordering = ['grid_filter_id']
    list_select_related = ['grid', 'grid_filter_field']

    def grid_name(self, gridfilter):
        return gridfilter.grid.name
    
    def grid_filter_field_name(self, gridfilter):
        return gridfilter.grid_filter_field.name


