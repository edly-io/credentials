"""
Badges app toggles.
"""

from edx_toggles.toggles import SettingToggle


# .. toggle_name: OPEN_BADGES_ENABLED
# .. toggle_implementation: DjangoSetting
# .. toggle_default: False
# .. toggle_description: Determines if the Credentials IDA uses open_badges functionality.
# .. toggle_life_expectancy: permanent
# .. toggle_permanent_justification: OpenBadges are optional for usage.
# .. toggle_creation_date: 2024-01-12
# .. toggle_use_cases: open_edx
ENABLE_OPEN_BADGES = SettingToggle("OPEN_BADGES_ENABLED", default=False, module_name=__name__)


def is_open_badges_enabled():
    """
    Check main feature flag.
    """

    return ENABLE_OPEN_BADGES.is_enabled()

def check_open_badges_enabled(func):
    """
    Decorator for checking the applicability of a badges app.
    """

    def wrapper(*args, **kwargs):
        if is_open_badges_enabled():
            return func(*args, **kwargs)
        return None

    return wrapper
