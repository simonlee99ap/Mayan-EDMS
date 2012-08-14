from __future__ import absolute_import

from django.db import transaction, DatabaseError
from django.utils.translation import ugettext_lazy as _

from job_processor.models import JobQueue, JobType
from job_processor.exceptions import JobQueuePushError
from navigation.api import bind_links, register_model_list_columns
from project_tools.api import register_tool
from project_setup.api import register_setup
from app_registry.api import register_app

from .links import backup_tool_link, restore_tool_link, backup_job_list, backup_job_create, backup_job_edit, backup_job_test
from .models import BackupJob

# TODO: move to literals
BACKUP_JOB_QUEUE_NAME = 'backups_queue'


@transaction.commit_on_success
def create_backups_job_queue():
    global backups_job_queue
    try:
        backups_job_queue, created = JobQueue.objects.get_or_create(name=BACKUP_JOB_QUEUE_NAME, defaults={'label': _('Backups'), 'unique_jobs': True})
    except DatabaseError:
        transaction.rollback()


create_backups_job_queue()
#backup_job_type = JobType('remote_backup', _(u'Remove backup'), do_backup)

register_setup(backup_tool_link)
register_tool(restore_tool_link)
bind_links([BackupJob, 'backup_job_list', 'backup_job_create'], [backup_job_list], menu_name='secondary_menu')
bind_links([BackupJob, 'backup_job_list', 'backup_job_create'], [backup_job_create], menu_name='sidebar')
bind_links([BackupJob], [backup_job_edit, backup_job_test])

register_model_list_columns(BackupJob, [
    {'name':_(u'begin date time'), 'attribute': 'begin_datetime'},
    {'name':_(u'storage module'), 'attribute': 'storage_module'},
])

register_app('backups', _(u'Backups'))
