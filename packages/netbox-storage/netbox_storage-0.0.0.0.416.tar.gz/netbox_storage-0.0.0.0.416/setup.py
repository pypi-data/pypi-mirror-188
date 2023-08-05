# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_storage',
 'netbox_storage.api',
 'netbox_storage.filters',
 'netbox_storage.forms',
 'netbox_storage.migrations',
 'netbox_storage.tables',
 'netbox_storage.views']

package_data = \
{'': ['*'],
 'netbox_storage': ['templates/netbox_storage/*',
                    'templates/netbox_storage/drive/*',
                    'templates/netbox_storage/inc/*',
                    'templates/netbox_storage/partition/*',
                    'templates/netbox_storage/physicalvolume/*',
                    'templates/netbox_storage/volumegroup/*']}

setup_kwargs = {
    'name': 'netbox-storage',
    'version': '0.0.0.0.416',
    'description': 'Netbox Storage Plugin',
    'long_description': '### Directory structure\n\n```\n+- api - The API type\n+- filters - Filters of the models\n+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm\n+- migrations - DB Django Migration\n+- tables - The ModelBaseTable, ModelTable, RelatedModelTable\n+- templates\n  +- netbox_disk - The detail view of each model\n    +- disk - The template content box in the Virtual Machine Model\n+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, \n           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView\n```\n### Models\n#### ERM\n\n\n#### Drive\nThe drive has 4 parameter:\n\n| Name           |           Example Value           |\n|:---------------|:---------------------------------:|\n| Virtualmachine | test-vm (Link zu virtual machine) |\n| Identifer      |           Festplatte 1            |\n| Cluster        |   STOR2000000 (Link zu cluster)   |\n| Size           |               50GB                |\n| System         |                No                 |\n\n#### Filesystem\nThe filesystem has 1 parameter:\n\n| Name | Example Value |\n|:-----|:-------------:|\n| fs   |     EXT4      |\n\n#### Linux Volume\nThe linux volume has 1 parameter:\n\n| Name            |       Example Value       |\n|:----------------|:-------------------------:|\n| vg_name         |          docker           |\n| lv_name         |          docker           |\n| Path            |      /var/lib/docker      |\n| Filesystem      | NTFS (Link zu Filesystem) |\n\n\n#### Windows Volume\nThe linux volume has 1 parameter:\n\n| Name       |        Example Value        |\n|:-----------|:---------------------------:|\n| drive_name |          (D, E, F)          |\n| Filesystem |  NTFS (Link zu Filesystem)  |\n\n\n\nBasis:\n- pv:\n  - size\n  - Storage Cluster\n  - virtual_machine\n\nWindows Form:\n- drive_name (D, E, F)\n- filesystem (ntfs)\n\nLinux Form:\n- vg name\n- lv name\n- path\n- filesystem\n\n\nExtra Filesystem Model & als ChoiceField ausgeben\n\n# Build\npoetry publish --build\ndocker-compose build --no-cache && docker-compose build --no-cache && docker-compose up -d\n\n<a href="{% url \'plugins:netbox_storage:physicalvolume_add\' %}?drive={{ object.id }}&pv_name={{ object.device_name }}&return_url={{ object.get_absolute_url }}" class="btn btn-sm btn-primary" role="button">\n    <i class="mdi mdi-plus-thick"></i> Add Physical Volume\n</a>\n\ngit add . && git commit -m "0.0.0.0.272" && git push\n\n\n[\n  [\n    Drive, Partition[]\n  ], \n  [\n    Drive, Partition[]\n  ]\n]',
    'author': 'Tim Rhomberg',
    'author_email': 'timrhomberg@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
