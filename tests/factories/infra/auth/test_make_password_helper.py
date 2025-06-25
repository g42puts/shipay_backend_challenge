from app.factories.infra.auth.make_password_helper import make_password_helper
from app.interfaces.password_helper import PasswordHelperInterface


def test_make_password_helper_should_return_password_helper_interface():
    password_helper = make_password_helper()
    assert isinstance(password_helper, PasswordHelperInterface)
