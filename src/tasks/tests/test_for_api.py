import uuid

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.models import Task
from datetime import datetime

URL = "http://localhost:8182/api/v1/tasks/"

@pytest.fixture
def user():
    return User.objects.create_user(username=f"testuser_{uuid.uuid4().hex}", password="testpassword")

@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def api_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

@pytest.fixture
def task_data():
    return {
        "title": "Test Task",
        "description": "Test description",
        "status": 1,
        "priority": 2,
    }

@pytest.fixture
def create_task(task_data):
    return Task.objects.create(**task_data)

def test_create_task(api_client, task_data):
    response = api_client.post(URL, task_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == task_data["title"]
    assert response.data["description"] == task_data["description"]
    assert response.data["status"] == task_data["status"]
    assert response.data["priority"] == task_data["priority"]

def test_get_task(api_client, create_task):
    url = f"{URL}{create_task.id}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == create_task.title
    assert response.data["description"] == create_task.description
    assert response.data["status"] == create_task.status
    assert response.data["priority"] == create_task.priority

def test_update_task(api_client, create_task):
    url = f"{URL}{create_task.id}/"
    updated_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": 2,
        "priority": 1,
    }
    response = api_client.put(url, updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == updated_data["title"]
    assert response.data["description"] == updated_data["description"]
    assert response.data["status"] == updated_data["status"]
    assert response.data["priority"] == updated_data["priority"]

def test_delete_task(api_client, create_task):
    url = f"{URL}{create_task.id}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=create_task.id).exists()

def test_task_created_at(api_client, task_data):
    response = api_client.post(URL, task_data, format="json")

    created_at = response.data["created_at"]
    assert created_at is not None
    assert isinstance(datetime.fromisoformat(created_at), datetime)

def test_task_updated_at(api_client, create_task):
    url = f"{URL}{create_task.id}/"
    updated_data = {"title": "Updated title"}
    response = api_client.patch(url, updated_data, format="json")

    updated_at = response.data["updated_at"]
    assert updated_at is not None
    assert isinstance(datetime.fromisoformat(updated_at), datetime)
