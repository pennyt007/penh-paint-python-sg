from django.db.models import Prefetch
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Grid, GridFilter, GridFilterField, Sidebar, SidebarButton, SidebarCarousel, SidebarItem
from . import serializers


class SidebarViewSet(ModelViewSet):
    queryset = Sidebar.objects.all()
    serializer_class = serializers.SidebarSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class GridViewSet(ModelViewSet):
    queryset = Grid.objects.all()
    serializer_class = serializers.GridSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class GridFilterFieldViewSet(ModelViewSet):
    queryset = GridFilterField.objects.all()
    serializer_class = serializers.GridFilterFieldSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class GridFilterViewSet(ModelViewSet):
    queryset = GridFilter.objects.select_related(
        'grid_filter_field').select_related('grid').all()
    serializer_class = serializers.GridFilterSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class SidebarCarouselViewSet(ModelViewSet):
    serializer_class = serializers.SidebarCarouselSerializer

    def get_queryset(self):
        return SidebarCarousel.objects\
            .filter(sidebar_id=self.kwargs['sidebar_pk'])\
            .select_related('sidebar')

    def get_serializer_context(self):
        return {'request': self.request}


class SidebarButtonViewSet(ModelViewSet):
    serializer_class = serializers.SidebarButtonSerializer

    def get_queryset(self):
        return SidebarButton.objects\
            .filter(sidebar_id=self.kwargs['sidebar_pk'])\
            .select_related('sidebar')

    def get_serializer_context(self):
        return {'request': self.request}


class SidebarItemViewSet(ModelViewSet):
    serializer_class = serializers.SidebarItemSerializer

    def get_queryset(self):
        return SidebarItem.objects\
            .filter(sidebar_id=self.kwargs['sidebar_pk'])\
            .select_related('sidebar')\
            .select_related('grid')\
            .order_by('order')

    def get_serializer_context(self):
        return {'request': self.request}


class SidebarItemWithGridFiltersViewSet(ModelViewSet):
    serializer_class = serializers.SidebarItemWithGridFiltersSerializer

    def get_queryset(self):
        queryset = SidebarItem.objects.filter(
            sidebar_id=self.kwargs['sidebar_pk']
        ).select_related('sidebar', 'grid')

        # Prefetch related GridFilter objects for each Grid associated with SidebarItems
        grid_filters_prefetch = Prefetch(
            'grid__gridfilter_set',
            queryset=GridFilter.objects.select_related('grid_filter_field'),
            to_attr='prefetched_grid_filters'
        )
        queryset = queryset.prefetch_related(grid_filters_prefetch)

        return queryset

class SidebarItemTreeViewSet(ModelViewSet):
    serializer_class = serializers.SidebarItemTreeSerializer

    def get_queryset(self):
        # Fetch root items and related data in a single query
        queryset = SidebarItem.objects.filter(parent_item__isnull=True, sidebar_id=self.kwargs['sidebar_pk']).select_related('sidebar', 'grid')
        # Prefetch children recursively to reduce queries
        prefetch_children = Prefetch(
            'children',
            queryset=SidebarItem.objects.select_related('sidebar', 'grid').order_by('order'),
            to_attr='prefetched_children'
        )

        queryset = queryset.prefetch_related(prefetch_children)
        
        return queryset

    def list(self, request, *args, **kwargs):
        root_items = self.get_queryset()
        serializer = self.get_serializer(root_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
