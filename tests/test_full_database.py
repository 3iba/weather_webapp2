
import os
import pytest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import databaseConnect, get_weather_table_data, delete_record

LOG_FILE = 'error.log'




@patch('database.mysql.connector.connect')
def test_valid_input(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, None]
    mock_cursor.lastrowid = 1

    try:
        databaseConnect("London", "UK", 18, "Cloudy")
    except Exception:
        pytest.fail("databaseConnect() вызвал исключение на корректных данных")

def test_negative_temperature_raises_value_error():
    with pytest.raises(ValueError):
        databaseConnect("Berlin", "Germany", -999, "Freezing")

def test_invalid_temperature_type():
    with pytest.raises(ValueError):
        databaseConnect("Tokyo", "Japan", "hot", "Sunny")

def test_empty_city_name():
    with pytest.raises(ValueError):
        databaseConnect("", "France", 20, "Mild")


@patch('database.mysql.connector.connect')
def test_get_weather_table_data_returns_correct_data(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_data = [
        {
            'city_name': 'Astana',
            'country': 'Kazakhstan',
            'temperature': 25,
            'description': 'Sunny',
            'weather_time': '12:00:00'
        }
    ]
    mock_cursor.fetchall.return_value = mock_data

    result = get_weather_table_data()
    assert result == mock_data
    mock_cursor.execute.assert_called_once()
    assert mock_conn.close.called

@patch('database.mysql.connector.connect')
def test_delete_record_deletes_correct_city(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    city_name = "Astana"
    delete_record(city_name)

    mock_cursor.execute.assert_any_call(
        'DELETE FROM weather WHERE city_id = (SELECT id FROM cities WHERE city_name = %s)',
        (city_name,)
    )
    mock_cursor.execute.assert_any_call(
        'DELETE FROM cities WHERE city_name = %s',
        (city_name,)
    )
    assert mock_conn.commit.called
    assert mock_conn.close.called

@patch('database.mysql.connector.connect')
def test_max_temperature(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, None]
    mock_cursor.lastrowid = 1

    try:
        databaseConnect("Dubai", "UAE", 60, "Hot")
    except Exception:
        pytest.fail("databaseConnect() вызвал исключение на граничном значении температуры")