from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from .tasks import basic, add, divide

class Task(models.Model):
    class Task_type(models.TextChoices):
        BASIC = 'BAS', _('Basic')
        ADD = 'ADD', _('Add')
        DIVIDE = 'DIV', _('Divide')

    class State(models.TextChoices):
        PENDING = 'PE', _('Pending')
        RUNNING = 'RU', _('Running')
        COMPLETED = 'CO', _('Completed')
        ERRORED = 'ER', _('Errored')

    id = models.BigAutoField(primary_key=True)

    task_type = models.CharField(
        max_length=3,
        choices=Task_type.choices,
        default=Task_type.BASIC,
        help_text="Type of the task"
    )

    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.PENDING,
        help_text="State of the task. a task can be ran when PENDING and available_at < now"
    )

    retry = models.IntegerField(
        default=1,
        help_text="Available retries before ERRORED"
    )

    data_input = models.JSONField()
    data_output = models.JSONField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available_at = models.DateTimeField(
        null=True,
        auto_now_add=True,
        help_text="Available_at must be below now for the task to be ran"
    )

    def __str__(self):
        return f"Task [{self.id}] '{self.get_task_type_display()}': {self.get_state_display()} @ {self.updated_at.strftime('%H-%M-%S')}"

    def runnable(self):
        return this.state == Task.State.PENDING and this.available_at < timezone.now()

    def run(self):
        # IMPROVEMENT: Modifying the Task_type enum to receive the task function would be valuable
        # https://stackoverflow.com/questions/64146651/how-can-i-subclass-django-textchoices-to-add-additional-attributes
        task_fns = {
            Task.Task_type.BASIC: basic,
            Task.Task_type.ADD: add,
            Task.Task_type.DIVIDE: divide,
        }
        return task_fns[self.task_type](self.data_input)
