
from mysite import create_app, tasks
app = create_app()
res = tasks.add.delay(2, 3)
print(res.get())
