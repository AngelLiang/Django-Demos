default_app_config = 'dictionary.apps.DictionaryConfig'


def get_dictionary(code):
    from .models import DictionarytItem
    from django.db.utils import OperationalError
    try:
        return tuple([(item.key, item.value) for item in DictionarytItem.objects.filter(master__code__exact=code)])
    except OperationalError:
        return None
