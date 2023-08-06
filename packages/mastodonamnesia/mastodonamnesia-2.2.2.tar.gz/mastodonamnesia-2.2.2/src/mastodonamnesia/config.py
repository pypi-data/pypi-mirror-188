# pylint: disable=E1136
"""This module contains helper classes and methods to assist with the general
function of this bot.

MastodonAmnesia - deletes old Mastodon toots
Copyright (C) 2021, 2022  Mark S Burgunder

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import logging
import os
import sys
from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar

import aiohttp
from minimal_activitypub import __display_name__ as ma_log_name
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError
from rich import print as rprint
from rich.logging import RichHandler

from . import __display_name__

BC = TypeVar("BC", bound="BotConfig")
ConfigClass = TypeVar("ConfigClass", bound="Configuration")
MC = TypeVar("MC", bound="MastodonConfig")

logger = logging.getLogger(__display_name__)


@dataclass
class BotConfig:
    """Dataclass holding configuration values for general behaviour of
    MastodonAmnesia."""

    # pylint: disable=too-many-instance-attributes
    log_level: str
    delete_after: int
    skip_deleting_pinned: Optional[bool]
    skip_deleting_faved: Optional[bool]
    skip_deleting_bookmarked: Optional[bool]
    skip_deleting_poll: Optional[bool]
    skip_deleting_dm: Optional[bool]
    skip_deleting_media: Optional[bool]
    skip_deleting_faved_at_least: Optional[int]
    skip_deleting_boost_at_least: Optional[int]

    def __init__(  # noqa: max-complexity: 12
        self: BC, config: Optional[dict[str, Any]]
    ) -> None:
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        # It's not that bad ;)
        if not config:
            config = {}

        self.log_level = config.get("log_level", "WARN")

        std_out_formatter = logging.Formatter(
            "%(name)s[%(process)d] %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
        )
        std_out_handler = RichHandler()
        std_out_handler.setFormatter(std_out_formatter)
        std_out_handler.setLevel(self.log_level)
        logger.addHandler(std_out_handler)

        self.delete_after = config.get("delete_after", None)
        self.skip_deleting_bookmarked = config.get("skip_deleting_bookmarked")
        self.skip_deleting_faved = config.get("skip_deleting_faved")
        self.skip_deleting_pinned = config.get("skip_deleting_pinned")
        self.skip_deleting_poll = config.get("skip_deleting_poll")
        self.skip_deleting_dm = config.get("skip_deleting_dm")
        self.skip_deleting_media = config.get("skip_deleting_media")
        self.skip_deleting_faved_at_least = config.get("skip_deleting_faved_at_least")
        self.skip_deleting_boost_at_least = config.get("skip_deleting_boost_at_least")

        if not self.delete_after:
            self._get_delete_after()

        if self.skip_deleting_bookmarked is None:
            self._get_skip_bookmarked()

        if self.skip_deleting_faved is None:
            self._get_skip_faved()

        if self.skip_deleting_pinned is None:
            self._get_skip_pinned()

        if self.skip_deleting_poll is None:
            self._get_skip_poll()

        if self.skip_deleting_dm is None:
            self._get_skip_dm()

        if self.skip_deleting_media is None:
            self._get_skip_media()

        if self.skip_deleting_faved_at_least is None:
            self._get_skip_faved_at_least()

        if self.skip_deleting_boost_at_least is None:
            self._get_skip_boost_at_lease()

    def _get_skip_poll(self: BC) -> None:
        """'Private' method to get skip deleting polls value from user if this
        value has not yet been configured."""
        rprint("Should polls be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_poll = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_poll = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_dm(self: BC) -> None:
        """'Private' method to get skip deleting 'private' messages value from
        user if this value has not yet been configured."""
        rprint("Should Direct Messages be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_dm = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_dm = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_media(self: BC) -> None:
        """'Private' method to get skip deleting toots with media value from
        user if this value has not yet been configured."""
        rprint(
            "Should Toots with attachements / pictures be deleted "
            "when they get old enough?"
        )
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_media = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_media = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_faved_at_least(self: BC) -> None:
        """'Private' method to get skip deleting toots that have been
        favourited value from user if this value has not yet been
        configured."""
        rprint(
            "Should Toots being favourited a certain mimimum number of times be "
            "excluded from deletion even when they get old enough?"
        )
        rprint("(enter 0 to disregard this setting)")
        self.skip_deleting_faved_at_least = int(input("[..] Please enter number: "))

    def _get_skip_boost_at_lease(self: BC) -> None:
        """'Private' method to get skip deleting toots that have been boosted
        value from user if this value has not yet been configured."""
        rprint(
            "Should Toots being boosted a certain mimimum number of times be "
            "excluded from deletion even when they get old enough?"
        )
        rprint("(enter 0 to disregard this setting)")
        self.skip_deleting_boost_at_least = int(input("[..] Please enter number: "))

    def _get_skip_pinned(self: BC) -> None:
        """'Private' method to get skip deleting pinned toots value from user
        if this value has not yet been configured."""
        rprint("Should pinned toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_pinned = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_pinned = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_faved(self: BC) -> None:
        """'Private' method to get skip deleting faveroited toots value from
        user if this value has not yet been configured."""
        rprint("Should favoured toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_faved = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_faved = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_skip_bookmarked(self: BC) -> None:
        """'Private' method to get skip deleting bookmarked toots from user if
        this value has not yet been configured."""
        rprint("Should bookmarked toots be deleted when they get old enough?")
        y_or_n = input("[..] Please enter Y for yes or N for no: ")
        if y_or_n in ("Y", "y"):
            self.skip_deleting_bookmarked = False
        elif y_or_n in ("N", "n"):
            self.skip_deleting_bookmarked = True
        else:
            rprint("! ERROR ... please only respond with 'Y' or 'N'")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

    def _get_delete_after(self: BC) -> None:
        """'Private' method to get delete after value from user if this value
        has not yet been configured."""
        rprint(
            "Please enter maximum age of retained toots in the "
            'format of "number unit"'
        )
        rprint('For example "1 weeks" or "3 days". Supported units are:')
        rprint(
            " - seconds\n"
            " - minutes\n"
            " - hours\n"
            " - days\n"
            " - weeks\n"
            " - months"
        )
        max_age = input("[..] Minimum age to delete toots (in seconds): ")
        max_age_parts = max_age.split(" ")
        max_age_number = int(max_age_parts[0])
        max_age_unit = max_age_parts[1]
        if max_age_unit == "seconds":
            self.delete_after = max_age_number
        elif max_age_unit == "minutes":
            self.delete_after = max_age_number * 3600
        elif max_age_unit == "hours":
            self.delete_after = max_age_number * 3600
        elif max_age_unit == "days":
            self.delete_after = max_age_number * 3600 * 24
        elif max_age_unit == "weeks":
            self.delete_after = max_age_number * 3600 * 24 * 7
        elif max_age_unit == "months":
            self.delete_after = max_age_number * 3600 * 24 * 30
        else:
            rprint("! Error ... unknown unit ({max_age_unit}) specified")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)


@dataclass
class MastodonConfig:
    """Dataclass holding configuration values for Mastodon settings."""

    instance: str
    access_token: str

    @classmethod
    async def load_mastodon_config(
        cls: Type[MC], mastodon_ini: Optional[dict[str, Any]]
    ) -> MC:
        """Loads Mastodon configuration from file and returns a MastodonConfig
        class instance."""

        logger.debug(
            "MastodonConfig.load_mastodon_config - mastodon_ini: %s", mastodon_ini
        )

        if not mastodon_ini:
            mastodon_ini = {}

        base_url = mastodon_ini.get("base_url", None)
        instance = mastodon_ini.get("instance", None)
        if instance is None and base_url:
            instance = base_url

        if not instance:
            instance = input(
                "[..] Enter instance (domain name) for Mastodon account host: "
            )

        access_token = mastodon_ini.get("access_token", None)

        user_info = mastodon_ini.get("user_info", None)
        if not access_token and user_info:
            access_token = user_info.get("access_token", None)

        try:
            if not access_token:
                user_name = input("[..] Enter user for your Fediverse account: ")
                password = input("[..] Enter password for your Fediverse account: ")

                async with aiohttp.ClientSession() as session:
                    access_token = await ActivityPub.get_auth_token(
                        instance_url=instance,
                        username=user_name,
                        password=password,
                        session=session,
                    )

        except ActivityPubError as error:
            rprint(f"! Error when setting up Fediverse connection: {error}")
            rprint("! Cannot continue. Exiting now.")
            sys.exit(1)

        return cls(instance=instance, access_token=access_token)


@dataclass
class Configuration:
    """Dataclass to hold all settings for tootbot."""

    bot: BotConfig
    mastodon: MastodonConfig

    @classmethod
    async def load_config(
        cls: Type[ConfigClass], config_file_name: str = "config.json"
    ) -> ConfigClass:
        """Loads configuration from file and returns a Configuration class
        instance."""
        if os.path.exists(config_file_name):
            with open(file=config_file_name, encoding="UTF-8") as config_file:
                loaded_config = json.load(config_file)
        else:
            loaded_config = {}

        mastodon_ini = loaded_config.get("mastodon")
        if not mastodon_ini:
            mastodon_ini = loaded_config.get("Mastodon")
        mastodon_config = await MastodonConfig.load_mastodon_config(
            mastodon_ini=mastodon_ini
        )

        bot_ini = loaded_config.get("bot")
        if not bot_ini:
            bot_ini = loaded_config.get("Bot")
        bot = BotConfig(config=bot_ini)

        config_instance = cls(bot=bot, mastodon=mastodon_config)
        config_dict = asdict(config_instance)
        with open(file=config_file_name, mode="w", encoding="UTF-8") as config_file:
            json.dump(config_dict, config_file, indent=4)
            logger.debug("Configuration.load_config - Saved config: %s", config_dict)

        return config_instance


async def setup_shop(
    config_file: str,
    debug_log_file: Optional[str],
) -> Configuration:
    """Processes command line arguments, establishes debug logging to file if
    specified, loads configuration.

    Returns:
        bool: true if this is a dry-run, i.e. no toots should be actually deleted.
        Configuration: config for this run of the MastodonAmnesia.
    """
    file_log_formatter = logging.Formatter(
        "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    if debug_log_file:
        file_handler = logging.FileHandler(filename=debug_log_file)
        file_handler.setFormatter(file_log_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        ma_logger = logging.getLogger(ma_log_name)
        ma_logger.setLevel(logging.DEBUG)
        ma_logger.addHandler(file_handler)

    config = await Configuration.load_config(config_file_name=config_file)
    return config
