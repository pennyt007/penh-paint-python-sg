from django_filters.rest_framework import FilterSet
from .models import SidebarItem

class SidebarItemFilter(FilterSet):
    class Meta:
        model = SidebarItem
        fields = {
            'sidebar_id': ['exact']
        }