### Directory structure

```
+- api - The API type
+- filters - Filters of the models
+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm
+- migrations - DB Django Migration
+- tables - The ModelBaseTable, ModelTable, RelatedModelTable
+- templates
  +- netbox_disk - The detail view of each model
    +- disk - The template content box in the Virtual Machine Model
+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, 
           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView
```
### Models
#### ERM


#### Drive
The drive has 4 parameter:

| Name           |           Example Value           |
|:---------------|:---------------------------------:|
| Virtualmachine | test-vm (Link zu virtual machine) |
| Identifer      |           Festplatte 1            |
| Cluster        |   STOR2000000 (Link zu cluster)   |
| Size           |               50GB                |
| System         |                No                 |

#### Filesystem
The filesystem has 1 parameter:

| Name | Example Value |
|:-----|:-------------:|
| fs   |     EXT4      |

#### Linux Volume
The linux volume has 1 parameter:

| Name            |       Example Value       |
|:----------------|:-------------------------:|
| vg_name         |          docker           |
| lv_name         |          docker           |
| Path            |      /var/lib/docker      |
| Filesystem      | NTFS (Link zu Filesystem) |


#### Windows Volume
The linux volume has 1 parameter:

| Name       |        Example Value        |
|:-----------|:---------------------------:|
| drive_name |          (D, E, F)          |
| Filesystem |  NTFS (Link zu Filesystem)  |



Basis:
- pv:
  - size
  - Storage Cluster
  - virtual_machine

Windows Form:
- drive_name (D, E, F)
- filesystem (ntfs)

Linux Form:
- vg name
- lv name
- path
- filesystem


Extra Filesystem Model & als ChoiceField ausgeben

# Build
poetry publish --build
docker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d

<a href="{% url 'plugins:netbox_storage:physicalvolume_add' %}?drive={{ object.id }}&pv_name={{ object.device_name }}&return_url={{ object.get_absolute_url }}" class="btn btn-sm btn-primary" role="button">
    <i class="mdi mdi-plus-thick"></i> Add Physical Volume
</a>

git add . && git commit -m "0.0.0.0.272" && git push


[
  [
    Drive, Partition[]
  ], 
  [
    Drive, Partition[]
  ]
]