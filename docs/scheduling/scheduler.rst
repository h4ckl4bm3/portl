=========
Scheduler
=========

In the previous section on Automation, the user could choose to run Services and Workflows immediately from their respective menus. Such an execution is performed without the help of the Scheduler and is simply a forked child process of portl. Alternatively, Services and Workflows can be scheduled by creating a Task, from the :guilabel:`scheduling/task_management` page. The task is then handed-off to the scheduler for managing its execution.

portl uses APScheduler to schedule Services and Workflows: https://apscheduler.readthedocs.io/en/latest/