"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance with a fresh app instance.
    Each test gets an isolated client to avoid state pollution.
    """
    return TestClient(app)
