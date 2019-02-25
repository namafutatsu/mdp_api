import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdp_api.settings")

from django.core.wsgi import get_wsgi_application  # pylint: disable=wrong-import-position

application = get_wsgi_application()
