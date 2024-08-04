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

# Improvements
To fit in the 2 hours limit, I did a lot of corner-cutting. Task model can be largely improved. The scheduler is missing a whole lot of utility function (pause, resume, stop, restart, refresh, ...). It is reaching the point where it is better to split it in multiple files.
Basic error checking is there but could be improved.
A proper logger is necessary.

1- tasks, model & fn
2- pool worker, assign task, lock it, and extract result
3- scheduler, get tasks, assign and lock them
4- insert new task