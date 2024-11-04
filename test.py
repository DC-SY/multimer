from datetime import datetime

from components.task_manager import *
from components.tag_manager import *
from components.tasks_tags_manager import *

# 获取全部任务
task_data = get_all_tasks()
# 获取全部标签
tag_data = get_all_tags()
# print(task_data)
# print(tag_data)


# 获取标签对应的任务
all_tasks_tags = get_all_task_tags()
print(all_tasks_tags)
