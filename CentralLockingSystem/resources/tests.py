from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from resources.models import Resource


class ResourceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.resource_name = "example_resource"
        self.resource_url = reverse('resource-detail', args=[self.resource_name])

    def test_put_acquire_resource(self):
        data = {
            "locked_by": "John Doe",
            "ttl": 60,
            "timeout": 120
        }
        response = self.client.put(self.resource_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"Success": "Resource is acquired."})

    def test_put_acquire_locked_resource_without_timeout(self):
        # First, acquire the resource
        data = {
            "locked_by": "John Doe",
            "ttl": 60,
            "timeout": 120
        }
        self.client.put(self.resource_url, data)

        # Then, try to acquire the locked resource without timeout
        response = self.client.put(self.resource_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"Error": "Resource is locked."})

    def test_put_acquire_locked_resource_with_timeout(self):
        # First, acquire the resource
        data = {
            "locked_by": "John Doe",
            "ttl": 60,
            "timeout": 1
        }
        self.client.put(self.resource_url, data)

        # Then, try to acquire the locked resource with timeout
        response = self.client.put(self.resource_url, data)
        self.assertEqual(response.status_code, status.HTTP_408_REQUEST_TIMEOUT)
        self.assertEqual(response.data, {"Error": "Request timed out."})

    def test_delete_release_resource(self):
        # First, acquire the resource
        data = {
            "locked_by": "John Doe",
            "ttl": 60,
            "timeout": 120
        }
        self.client.put(self.resource_url, data)

        # Then, release the resource
        response = self.client.delete(self.resource_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"Success": "Resource is released."})

    def test_delete_release_unlocked_resource(self):
        response = self.client.delete(self.resource_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"Error": "Resource is not acquired."})

    def test_delete_release_resource_with_invalid_unlock_request(self):
        # First, acquire the resource
        data = {
            "locked_by": "John Doe",
            "ttl": 60,
            "timeout": 120
        }
        self.client.put(self.resource_url, data)

        # Then, try to release the resource with invalid unlock request
        invalid_data = {
            "locked_by": "Jane Smith"
        }
        response = self.client.delete(self.resource_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"Error": "Invalid unlock request."})
