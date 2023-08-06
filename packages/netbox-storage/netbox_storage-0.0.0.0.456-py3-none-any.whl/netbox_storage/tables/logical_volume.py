import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
    ActionsColumn,
)

from netbox_storage.models import LogicalVolume


class LogicalVolumeTable(NetBoxTable):
    """Table for displaying LogicalVolume objects."""

    pk = ToggleColumn()
    fs = tables.Column(
        linkify=True,
        verbose_name="Filesystem"
    )
    vg = tables.Column(
        linkify=True,
        verbose_name="Volume Group Name"
    )
    lv_name = tables.Column(
        linkify=True,
        verbose_name="Logical Volume Name"
    )

    class Meta(NetBoxTable.Meta):
        model = LogicalVolume
        fields = (
            "pk",
            "vg",
            "lv_name",
            "path",
            "fs",
            "description",
        )
        default_columns = (
            "vg",
            "lv_name",
            "path",
            "fs",
            "description"
        )
