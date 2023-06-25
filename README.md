# README.md

## Central Locking System

This application provides a central locking system to track the status of different types of resources, whether they're held by one of our services/processes or not. The system is exposed via REST API endpoints that allow to acquire or release a resource given its name.

---

### Prerequisites
- Python 3.8 or later.
- Poetry
- Django framework.
- Django Rest Framework.
- Django Environ

---

### Installation
1. Clone this repository:
    ```
    git clone <repository_link>
    ```
2. Navigate to the project directory:
    ```
    cd CentralLockingSystem
    ```
3. Install dependencies:
    ```
      poetry install #you can use the requirements.txt file but make sure to create a virtual envinrnoment
    ```
4. Activate the environment:
    ```
      poetry shell 
    ```
5. Run migrations:
    ```
    python manage.py migrate
    ```
6. Run the server:
    ```
    python manage.py runserver
    ```

---

### API Endpoints

The following API endpoints are provided:

1. `PUT /resources/{resource_name}/`: Acquires a resource.

    Request Parameters:
    - `locked_by` (required): Unique locking key of the service or process that is attempting to acquire the resource.
    - `ttl` (optional): Time-to-live, in seconds, for which the resource should be locked.
    - `timeout` (optional): Time, in seconds, the caller should wait if the resource is already locked.

    Response:
    - `200 OK`: Resource is successfully acquired.
    - `400 Bad Request`: Resource is already locked and no timeout was provided.
    - `408 Request Timeout`: The request timed out while waiting for the resource to become available.

2. `DELETE /resources/{resource_name}/`: Releases a resource.

    Request Parameters:
    - `locked_by` (required): Identifier of the service or process that is attempting to release the resource.

    Response:
    - `204 No Content`: Resource is successfully released.
    - `400 Bad Request`: Resource is not locked, or the caller does not have permission to release the resource.

---

### Example Usage

The API can be used via any HTTP client. Here are some examples using curl:

Acquire a resource:
```shell
curl -X PUT http://localhost:8000/resources/{resource_name}/ \
     -H "Content-Type: application/json" \
     -d '{
           "locked_by": "passCode@!",
           "ttl": 60,
           "timeout": 10
         }'
```

Release a resource:
```shell
curl -X DELETE http://localhost:8000/resources/{resource_name}/ \
     -H "Content-Type: application/json" \
     -d '{
           "locked_by": "passCode@!"
         }'
```

Replace `{resource_name}` with the name of the resource you want to acquire or release.

---

### Unit Tests
To run the unit tests, use the following command:

```shell
python manage.py test
```

---

### Resources
- [poetry installation](https://python-poetry.org/docs/)

---

### PS
For completeness, I should note that this code only provides a basic solution. A production solution would need to handle more edge cases, possibly have better efficiency, and be more secure. For example, in this code, a resource can be unlocked by anyone, not just the service that locked it. You would probably want to add more security in a real-world solution.

The TTL functionality is also implemented in a quite naive way here, just to show the concept. In a real-world scenario, you should consider more robust and scalable ways to handle TTLs.


--
