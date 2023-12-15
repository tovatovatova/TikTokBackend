from lib.user_config import UserConfig


# Test the initialization of the UserConfig class
def test_user_config_initialization():
    user_config = UserConfig(lang="en", platform="web")
    assert user_config.lang == "en"
    assert user_config.platform == "web"


# Test the initialization with different values
def test_user_config_initialization_different_values():
    user_config = UserConfig(lang="fr", platform="mobile")
    assert user_config.lang == "fr"
    assert user_config.platform == "mobile"
