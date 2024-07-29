from django.apps import AppConfig

from credentials.apps.open_badges.toggles import check_open_badges_enabled


class OpenBadgesConfig(AppConfig):
    """
    Core badges application configuration.
    """

    name = "credentials.apps.open_badges"
    verbose_name = "OpenBadges"

    @check_open_badges_enabled
    def ready(self):
        """
        Performs initial registrations for checks, signals, etc.
        """

        from credentials.apps.badges import signals # pylint: disable=unused-import,import-outside-toplevel
        from credentials.apps.open_badges.handlers import (  # pylint: disable=import-outside-toplevel
            listen_to_badging_events,
        )

        listen_to_badging_events()

        super().ready()
