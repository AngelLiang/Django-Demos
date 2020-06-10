
## 快速开始

    pipenv install
    pipenv shell
    python manage.py migrate
    python manage.py bootstrap
    python manage.py order_bootstrap
    python manage.py runserver


- root/q1w2e3r4
- admin/q1w2e3r4
- team_leader_1/q1w2e3r4
- purchaser_1/q1w2e3r4
- developer_1/q1w2e3r4

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


## hook function example

```python
from datetime import datetime

def handle(context):
    print(datetime.now())
```


```python
from river.models.hook import BEFORE, AFTER

def _handle_my_transitions(hook):
    workflow = hook['payload']['workflow']
    workflow_object = hook['payload']['workflow_object']
    source_state = hook['payload']['transition_approval'].meta.transition_meta.source_state
    destination_state = hook['payload']['transition_approval'].meta.transition_meta.destination_state
    last_approved_by = hook['payload']['transition_approval'].transactioner
    if hook['when'] == BEFORE:
        print('A transition from %s to %s will soon happen on the object with id:%s and field_name:%s!' % (source_state.label, destination_state.label, workflow_object.pk, workflow.field_name))
    elif hook['when'] == AFTER:
        print('A transition from %s to %s has just happened on the object with id:%s and field_name:%s!' % (source_state.label, destination_state.label, workflow_object.pk, workflow.field_name))
    print('Who approved it lately is %s' % last_approved_by.username)

def _handle_my_approvals(hook):
    workflow = hook['payload']['workflow']
    workflow_object = hook['payload']['workflow_object']
    approved_by = hook['payload']['transition_approval'].transactioner
    if hook['when'] == BEFORE:
        print('An approval will soon happen by %s on the object with id:%s and field_name:%s!' % ( approved_by.username, workflow_object.pk, workflow.field_name ))
    elif hook['when'] == AFTER:
        print('An approval has just happened by %s  on the object with id:%s and field_name:%s!' % ( approved_by.username, workflow_object.pk, workflow.field_name ))

def _handle_completions(hook):
    workflow = hook['payload']['workflow']
    workflow_object = hook['payload']['workflow_object']
    if hook['when'] == BEFORE:
        print('The workflow will soon be complete for the object with id:%s and field_name:%s!' % ( workflow_object.pk, workflow.field_name ))
    elif hook['when'] == AFTER:
        print('The workflow has just been complete for the object with id:%s and field_name:%s!' % ( workflow_object.pk, workflow.field_name ))

def handle(context):
    hook = context['hook']
    if hook['type'] == 'on-transit':
        _handle_my_transitions(hook)
    elif hook['type'] == 'on-approved':
        _handle_my_approvals(hook)
    elif hook['type'] == 'on-complete':
        _handle_completions(hook)
    else:
        print("Unknown event type %s" % hook['type'])
```

---

- doc: https://django-river.readthedocs.io/

