from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import LogicalVolume


class LogicalVolumeFilter(NetBoxModelFilterSet):
    """Filter capabilities for LogicalVolume instances."""

    class Meta:
        model = LogicalVolume
        fields = [
            "vg",
            "lv_name",
            "fs",
            "path",
            "description"
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(vg__icontains=value)
            | Q(lv_name__icontains=value)
            | Q(fs__icontains=value)
            | Q(path__icontains=value)
        )
        return queryset.filter(qs_filter)
