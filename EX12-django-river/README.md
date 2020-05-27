
## 快速开始

    pipenv install
    pipenv shell
    python manage.py migrate
    python manage.py bootstrap


- root/q1w2e3r4
- team_leader_1/q1w2e3r4
- purchaser_1/q1w2e3r4


## river 使用说明

1. Install and enable it

```
pip install django-river river-admin
```

```
INSTALLED_APPS = [
    ...
    'river',
    'river-admin',
    ...
]
```

2. Create your first `state` machine in your model and migrate your db

    from django.db import models
    from river.models.fields.state import StateField

    class MyModel(models.Model):
        my_state_field = StateField()

3. Create all your states on the admin page

4. Create a `workflow` with your model ( `MyModel` - `my_state_field` ) information on the admin page

5. Create your `transition metadata` within the workflow created earlier, source and destination states

6. Create your `transition approval metadata` within the workflow created earlier and authorization rules along with their priority on the admin page

7. Enjoy your `django-river` journey.

---

- doc: https://django-river.readthedocs.io/

