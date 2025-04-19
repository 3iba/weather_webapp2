import pytest
from unittest.mock import patch, MagicMock
from weather_api import get_weather


@patch('weather_api.database.databaseConnect')
@patch('weather_api.requests.get')
def test_get_weather_valid_data(mock_get, mock_database_connect):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'cod': 200,
        'name': 'London',
        'sys': {'country': 'GB'},
        'main': {'temp': 18.5},
        'weather': [{'description': 'cloudy'}]
    }
    mock_get.return_value = mock_response

    result = get_weather("London", "valid_api_key")

    assert result == {
        'city': 'London',
        'temperature': 18.5,
        'description': 'Cloudy'
    }
    mock_database_connect.assert_called_once_with('London', 'GB', 18.5, 'Cloudy')


@patch('weather_api.database.databaseConnect')
@patch('weather_api.requests.get')
def test_get_weather_invalid_api_key(mock_get, mock_database_connect):
    mock_response = MagicMock()
    mock_response.json.return_value = {'cod': 401}
    mock_get.return_value = mock_response

    result = get_weather("London", "invalid_api_key")
    assert result['error'] == "Ошибка! Неверный API-ключ"
    mock_database_connect.assert_not_called()


@patch('weather_api.database.databaseConnect')
@patch('weather_api.requests.get')
def test_get_weather_city_not_found(mock_get, mock_database_connect):
    mock_response = MagicMock()
    mock_response.json.return_value = {'cod': '404'}
    mock_get.return_value = mock_response

    result = get_weather("UnknownCity", "valid_key")
    assert result['error'] == "Ошибка! Неверное название города"
    mock_database_connect.assert_not_called()


@patch('weather_api.database.databaseConnect')
@patch('weather_api.requests.get')
def test_get_weather_empty_data(mock_get, mock_database_connect):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    with pytest.raises(KeyError):
        get_weather("City", "key")
    mock_database_connect.assert_not_called()


@patch('weather_api.database.databaseConnect')
@patch('weather_api.requests.get')
def test_get_weather_network_error(mock_get, mock_database_connect):
    mock_get.side_effect = Exception("Сетевая ошибка")

    result = get_weather("City", "key")
    assert result['error'] == "Ошибка сети"
    mock_database_connect.assert_not_called()
