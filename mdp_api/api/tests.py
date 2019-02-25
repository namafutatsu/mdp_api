from django.test import TestCase

from . import models


class NameSlugMixinTestCase(TestCase):

    def test_slug_is_updated(self):
        # Test slug is generated upon create
        slug_model = models.Organization.objects.create(name="Hello World")
        self.assertEqual(slug_model.slug, 'hello-world')

        # Test slug is updated accordingly if the same slug already exists
        slug_model_bis = models.Organization.objects.create(name="Hello World")
        self.assertEqual(slug_model_bis.slug, 'hello-world-1')

        # Check a double save does not change the slug
        slug_model.save()
        self.assertEqual(slug_model.slug, 'hello-world')

        # Check slug is updated upon save if name is changed
        slug_model.name = "And now, completely different !"
        slug_model.save()
        self.assertEqual(slug_model.slug, 'and-now-completely-different')

        # Test the force_save resets the slugs also
        models.Organization.objects.update(name='One last time ...')
        models.force_save_all_models()
        slug_model.refresh_from_db()
        self.assertEqual(slug_model.slug, 'one-last-time')
