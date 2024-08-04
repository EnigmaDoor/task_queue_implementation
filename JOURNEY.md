# Celery
Celery is the go-to for this usecase. If this were a real need, we could correctly use Celery. Here, Celery (or plenty of other packages) would realize too much of the project so I'll stay away from it and try to use more native tools.

# Boilerplate selection
While I understand a web framework wasn't needed on this techtest, a quick boilerplate could add a lot of value and ease of use for a small time spent. As you say it is a first step to lead into a system deployable in production, I figured that in this case the time spent was worth it.
I went and selected a very lightweight boilerplate: https://github.com/AGTGreg/DjangoBoilerplate - Mostly to skip the postgres & docker implementation, a staple on most projects I start.
I ultimately had to adapt this boilerplate a bit to avoid a manual initialization step with docker.

# Scheduler
I went for a time-scheduled scheduler with python's concurrent threadpool, grabbing any runnable tasks and inserting them in the worker pool.
A task loop is ran often to grab any new task to be ran. An easy improvement could be to trigger that task loop when inserting a new task.
A cleaner loop is ran to ensure all tasks are within parameter (auto-failing tasks running for a long time).
Tasks have an auto-retry and back-off system, which can very easily be configured as an improvement.

# CRUD
The crud is very barebone but present (for create & show), you can check localhost:8000 while running to access the tasks and add some. Thanks https://github.com/prosenjeetshil/django-crud-operations-tutorial for the layout.

# Improvements
To fit in the 2 hours limit, I did a lot of corner-cutting. In order of importance, here are th improvements possible to better reach a production system.
- Testing first of all
- Implementing an actual task system such as Celery, as the only reason it wasn't done here was to do the exercice. Redis is already present and setup for us to use it with Celery. If we for some reason forgo Celery to improve that custom tasks system, then better task tracking is necessary, along with a scheduler able to receive triggers instead of only a time schedule.
- Task model can be largely improved. The scheduler is missing a whole lot of utility function (pause, resume, stop, restart, refresh, ...). It is reaching the point where it is better to split it in multiple files.Basic error checking is there but could be improved.
- Better separation of concerns between Task & Scheduler.
- A proper logger is necessary.
- The CRUD is barebone & basic.
