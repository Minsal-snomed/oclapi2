import logging

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from core.bundles.serializers import FHIRBundleSerializer
from core.code_systems.views import CodeSystemValidateCodeView
from core.collections.models import Collection, default_expansion_parameters
from core.collections.views import CollectionListView, CollectionRetrieveUpdateDestroyView, \
    CollectionVersionExpansionsView
from core.common.constants import HEAD
from core.common.fhir_helpers import translate_fhir_query
from core.concepts.views import ConceptRetrieveUpdateDestroyView
from core.sources.models import Source
from core.value_sets.serializers import ValueSetDetailSerializer, \
    ValueSetExpansionParametersSerializer, ValueSetExpansionSerializer

logger = logging.getLogger('oclapi')


class ValueSetListView(CollectionListView):
    serializer_class = ValueSetDetailSerializer

    @staticmethod
    def bundle_response(data, paginator):
        bundle = FHIRBundleSerializer(
            {'meta': {}, 'type': 'searchset', 'entry': FHIRBundleSerializer.convert_to_entry(data)},
            context={'paginator': paginator}
        )
        return bundle.data

    def get_filter_params(self, default_version_to_head=True):
        return super().get_filter_params(False)

    def apply_query_filters(self, queryset):
        query_fields = list(self.serializer_class.Meta.fields)

        queryset = translate_fhir_query(query_fields, self.request.query_params, queryset)

        return queryset

    def apply_filters(self, queryset):
        queryset = queryset.exclude(version=HEAD).filter(is_latest_version=True)
        return self.apply_query_filters(queryset)

    def get_serializer_class(self):
        return self.serializer_class

    def get_detail_serializer(self, obj):
        return self.serializer_class(obj)


class ValueSetValidateCodeView(CodeSystemValidateCodeView):

    def get_queryset(self):
        queryset = super(ConceptRetrieveUpdateDestroyView, self).get_queryset()

        parameters = self.get_parameters()

        url = parameters.get('url')
        code = parameters.get('code')
        system = parameters.get('system')
        display = parameters.get('display')
        system_version = parameters.get('systemVersion')

        if url:
            collection = Collection.objects.filter(canonical_url=url).exclude(version=HEAD)\
                .filter(is_latest_version=True)
            if not collection:
                return queryset.none()
            queryset = queryset.filter(references__collection=collection.first())

        if code and system:
            concept_source = Source.objects.filter(canonical_url=system)
            if not concept_source:
                return queryset.none()
            if system_version:
                concept_source = concept_source.filter(version=system_version)
            else:
                concept_source = concept_source.filter(is_latest_version=True).exclude(version=HEAD)
            if concept_source:
                queryset = queryset.filter(sources=concept_source.first(), mnemonic=code)
            else:
                return queryset.none()

        if display:
            instance = queryset.first()
            if display not in (instance.name, instance.display_name):
                return queryset.none()

        return queryset


class ValueSetRetrieveUpdateView(CollectionRetrieveUpdateDestroyView):
    serializer_class = ValueSetDetailSerializer

    def get_filter_params(self, default_version_to_head=True):
        return super().get_filter_params(False)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == 'DELETE':
            return queryset  # Delete HEAD with all versions

        return queryset.exclude(version=HEAD)

    def get_detail_serializer(self, obj):
        return ValueSetDetailSerializer(obj)


class ValueSetExpandView(CollectionVersionExpansionsView):
    sync = True

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ValueSetExpansionParametersSerializer

        return ValueSetExpansionSerializer

    def get_response_serializer_class(self):
        return ValueSetExpansionSerializer

    def get_filter_params(self, default_version_to_head=True):
        # Método modificado para incluir tu lógica de extracción de parámetros
        query_params = self.request.query_params.dict()

        version = query_params.get('version', None) or self.kwargs.get('version', None)
        if not version and default_version_to_head:
            version = HEAD

        kwargs = self.kwargs.copy()
        if self.user_is_self and self.request.user.is_authenticated:
            kwargs['user'] = self.request.user.username

        return {
            **query_params.copy(), **kwargs,
            'version': version, 'include_references': self.should_include_references()
        }

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        queryset = queryset.exclude(version=HEAD).filter(is_latest_version=True)[:1]
        return queryset

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.method == 'GET':
            filter_param = self.request.query_params.get('filter', None)  # Obtener el parámetro 'filter'

            if filter_param:
                # Asumiendo que 'display_name' es el campo a filtrar, ajusta según sea necesario
                qs = qs.filter(display_name__icontains=filter_param)

        return qs

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)
