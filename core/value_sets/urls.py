from django.urls import re_path

from core.common.constants import NAMESPACE_PATTERN
from . import views

from .views import ValueSetListView  # Import the ValueSetListView class

# Define the URL patterns for the value_sets app.
urlpatterns = [
    re_path(r'^$', views.ValueSetListView.as_view(),
            name='value-set-list'),

    re_path(fr"^(?P<collection>{NAMESPACE_PATTERN})/\$validate-code/$", views.ValueSetValidateCodeView.as_view(),
            name='value-set-validate-code'),

    re_path(fr"^(?P<collection>{NAMESPACE_PATTERN})/\$expand/$", views.ValueSetExpandView.as_view(),
            name='value-set-expand'),

    re_path(r"^\$validate-code/$", views.ValueSetValidateCodeView.as_view(),
            name='value-set-validate-code-global'),

    re_path(r"^\$expand/$", views.ValueSetExpandView.as_view(),
            name='value-set-expand-global'),

    re_path(
        fr"^(?P<collection>{NAMESPACE_PATTERN})/$", views.ValueSetRetrieveUpdateView.as_view(),
            name='value-set-detail'),
]
