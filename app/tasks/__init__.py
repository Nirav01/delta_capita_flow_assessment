from .flow_tasks import task1, task2, task3

# simple registry: task name in JSON -> function
registry = {
    "task1": task1,
    "task2": task2,
    "task3": task3,
}
