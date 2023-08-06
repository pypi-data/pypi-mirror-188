import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import VolumeGroup


class VolumeGroupTable(NetBoxTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()
    vg_name = tables.Column(
        linkify=True,
        verbose_name="Volume Group Name"
    )

    class Meta(NetBoxTable.Meta):
        model = VolumeGroup
        fields = (
            "pk",
            "vg_name",
            "description",
        )
        default_columns = (
            "vg_name",
            "description"
        )
