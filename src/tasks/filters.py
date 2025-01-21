import django_filters

from tasks.models import Task


class TasksFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='exact')
    priority = django_filters.CharFilter(lookup_expr='exact')
    created_at = django_filters.DateFilter(lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'created_at']