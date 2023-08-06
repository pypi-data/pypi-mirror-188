from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import Drive, Filesystem
from virtualization.models import Cluster, ClusterType, VirtualMachine


class LVMSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    lv_name = CharField(
        label="LV Name",
        help_text="Logical Volume Name e.g. lv_docker",
    )
    vg_name = CharField(
        label="VG Name",
        help_text="Volume Group Name e.g. vg_docker",
    )
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "cluster_type",
                "cluster",
                "virtual_machine",
            ),
        ),
        (
            "Drive Configuration",
            (
                "lv_name",
                "vg_name",
                "size",
                "path",
                "fs",
                "description",
            ),
        ),
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class LVSimpleForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the logical volume e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    path = CharField(
        label="Path",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    fs = DynamicModelChoiceField(
        queryset=Filesystem.objects.all(),
        label="Filesystem Name",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:filesystem-list")}
        ),
        help_text="The Filesystem of the Volume e.g. ext4",
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Cluster Config",
            (
                "cluster_type",
                "cluster",
                "virtual_machine",
            ),
        ),
        (
            "Drive Configuration",
            (
                "size",
                "path",
                "fs",
                "description",
            ),
        ),
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )
