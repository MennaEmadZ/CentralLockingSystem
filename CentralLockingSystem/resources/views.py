from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import Resource
from .serializers import ResourceSerializer
import time


class ResourceView(APIView):

    # In the context of the task,
    # when we "acquire" a resource, we are essentially updating the state of an existing resource rather than creating a new one
    # but to simplify the solution as possible we will use get_or_create() instead of get()
    def get_object(self, name):
        try:
            resource, created = Resource.objects.get_or_create(name=name, defaults={'locked_by': 'default', 'ttl': 0, "timeout": 0})
            return resource
        except Resource.DoesNotExist:
            raise NotFound('A resource with this name does not exist.')

    def put(self, request, name):
        resource = self.get_object(name)

        # # if the get_object was get the bellow comment will be uncommented
        # if resource is None:
        #     return Response({"error": "Resource not found."}, status=404)

        ttl = int(request.data.get("ttl")) if request.data.get("ttl") else None
        timeout = int(request.data.get("timeout")) if request.data.get("timeout") else None

        if cache.get(name):
            if not timeout:  # If there is no timeout, return immediately
                return Response({"Error": "Resource is locked."}, status=400)
            else:  # If there is a timeout, enter a loop to wait
                start_time = time.time()
                while cache.get(name):
                    if time.time() - start_time > timeout:
                        return Response({"Error": "Request timed out."}, status=408)
                    time.sleep(1)

        cache.set(name, request.data.get("locked_by"), ttl)
        serializer_data = request.data.copy()
        serializer_data['name'] = name
        serializer = ResourceSerializer(resource, data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Resource is aquired."})
        return Response(serializer.errors, status=400)

    def delete(self, request, name):
        resource = self.get_object(name)
        if cache.get(name) is None:
            return Response({"Error": "Resource is not aquired."}, status=400)
        if cache.get(name) != request.data.get("locked_by"):
            return Response({"Error": "Invalid unlock request."}, status=400)
        cache.delete(name)
        resource.delete()
        return Response({"Success": "Resource is released."},status=204)
