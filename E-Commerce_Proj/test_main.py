from unittest.mock import MagicMock
import pytest
import requests

from main import get_json_data

def test_get_json_data(monkeypatch):
    fake_data = {"products": 
                 [{"id": 1, "title": "Fake Product", "price": 10.0, "stock": 5}]
                 }
    fake_response = MagicMock()
    fake_response.json.return_value = fake_data
    monkeypatch.setattr(requests,"get", lambda url: fake_response)
    result = get_json_data()
    assert result == fake_data["products"]
    assert len(result) == 1
    assert result[0]["title"] == "Fake Product"

