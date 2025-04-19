import os
import logging
import weather_api
from unittest.mock import patch


@patch('weather_api.requests.get', side_effect=Exception("Симулированная ошибка сети"))
def test_logging_on_network_error(mock_get):
    log_file = 'error.log'

    weather_api.get_weather("Astana", "test_key")

    assert os.path.exists(log_file)

    with open(log_file, 'r', encoding='utf-8') as f:
        log_contents = f.read()

    assert "Ошибка сети при запросе погоды для города Astana" in log_contents
    assert "Симулированная ошибка сети" in log_contents
