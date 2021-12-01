import django_filters
from django.db.models import Q


class SearchFilterSet(django_filters.FilterSet):
    """Base search filter set. It uses __icontains lookup,
    so it must be used only for CharField or other text
    fields that support __icontains.

    This filter set filter for attributes described in
    ``search_fields``.
    """
    search = django_filters.CharFilter(method='filter_search')
    search_fields = ()
    int_fields = ()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        query = Q()
        for v in self.search_fields:
            query |= Q(**{f"{v}__icontains": value})

        for v in self.int_fields:
            try:
                value = int(value)
            except ValueError:
                continue
            query |= Q(**{v: value})

        return queryset.filter(query).distinct()

    def filter_integer(self, queryset, name, value):
        if not value:
            return queryset
        query = Q()
        for v in self.int_fields:
            query |= Q(**{v: value})

        return queryset.filter(query).distinct()


class ProductFilter(SearchFilterSet):
    ordering = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('price', 'price'),
        ),
    )
    search_fields = ('name', 'description', 'country_producer__name')
