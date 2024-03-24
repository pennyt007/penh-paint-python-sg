from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('sidebars', views.SidebarViewSet)

sidebars_router = routers.NestedDefaultRouter(
    router, 'sidebars', lookup='sidebar')
sidebars_router.register(
    'carousels', views.SidebarCarouselViewSet, basename='sidebar-carousels')
sidebars_router.register(
    'buttons', views.SidebarButtonViewSet, basename='sidebar-buttons')
sidebars_router.register(
    'items', views.SidebarItemViewSet, basename='sidebar-items')
sidebars_router.register('itemswithgridfilters', views.SidebarItemWithGridFiltersViewSet,
                         basename='sidebar-itemswithgridfilters')
sidebars_router.register(
    'itemsastree', views.SidebarItemTreeViewSet, basename='sidebar-itemsastree')

urlpatterns = router.urls + sidebars_router.urls
