from rest_framework.test import APITestCase
from django.urls import reverse
import pytest


pytestmark = [pytest.mark.django_db]
EVERYTHING_EQUALS_NON_NONE = type('omnieq', (), {"__eq__": lambda x, y: y is not None})()


class SomeTest(APITestCase):
    fixtures = ['api/tests/fixtures/fixture_categories.json']

    def test_categories_all_view(self):
        viewset_url = reverse('categories-all')

        response = self.client.get(viewset_url)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "name": "category1",
                "description": EVERYTHING_EQUALS_NON_NONE
            },
            {
                "id": 2,
                "name": "category2",
                "description": EVERYTHING_EQUALS_NON_NONE
            },
            {
                "id": 3,
                "name": "category3",
                "description": EVERYTHING_EQUALS_NON_NONE
            }

        ]


