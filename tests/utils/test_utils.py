from app.utils.utils import get_current_datetime_formatted


def test_get_current_datetime_formatted():
    current_datetime_formatted = get_current_datetime_formatted()
    assert current_datetime_formatted