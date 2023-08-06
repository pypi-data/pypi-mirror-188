from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import asyncstdlib
from asyncstdlib import heapq
from discord.app_commands import Choice, Transformer
from discord.ext import commands
from rapidfuzz import fuzz

from pylav.exceptions.database import EntryNotFoundException
from pylav.extension.radio.objects import Codec, Country, CountryCode, Language, State, Station, Tag
from pylav.helpers.format.strings import shorten_string
from pylav.logging import getLogger
from pylav.type_hints.bot import DISCORD_CONTEXT_TYPE, DISCORD_INTERACTION_TYPE

try:
    from redbot.core.i18n import Translator  # type: ignore

    _ = Translator("PyLav", Path(__file__))
except ImportError:
    Translator = None

    def _(string: str) -> str:
        return string


LOGGER = getLogger("PyLav.extension.Shared.converters.radio")

if TYPE_CHECKING:

    StationConverter = TypeVar("StationConverter", bound=list[Station])
    TagConverter = TypeVar("TagConverter", bound=list[Tag])
    LanguageConverter = TypeVar("LanguageConverter", bound=list[Language])
    StateConverter = TypeVar("StateConverter", bound=list[State])
    CodecConverter = TypeVar("CodecConverter", bound=list[Codec])
    CountryCodeConverter = TypeVar("CountryCodeConverter", bound=list[CountryCode])
    CountryConverter = TypeVar("CountryConverter", bound=list[Country])
else:

    class StationConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[Station]:
            """Converts a station name to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                return await ctx.pylav.radio_browser.station_by_uuid(
                    arg
                ) or await ctx.pylav.radio_browser.stations_by_name(name=arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Station with name `{arg}` not found").format(arg=arg)) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[Station]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            data = interaction.data
            options = data.get("options", [])
            kwargs = {"order": "votes"}
            if options:
                country_code = [v for v in options if v.get("name") == "countrycode"]
                country = [v for v in options if v.get("name") == "country"]
                state = [v for v in options if v.get("name") == "state"]
                language = [v for v in options if v.get("name") == "language"]
                tags = [v for v in options if v.get("name", "").startswith("tag")]
                if country_code and (val := country_code[0].get("value")):
                    kwargs["countrycode"] = val
                if country and (val := country[0].get("value")):
                    kwargs["country"] = val
                    kwargs["country_exact"] = any(
                        True for c in await interaction.client.pylav.radio_browser.countries() if c.name == val
                    )
                if state and (val := state[0].get("value")):
                    kwargs["state"] = val
                    kwargs["state_exact"] = any(
                        True for t in await interaction.client.pylav.radio_browser.states() if t.name == val
                    )
                if language and (val := language[0].get("value")):
                    kwargs["language"] = val
                    kwargs["language_exact"] = any(
                        True for t in await interaction.client.pylav.radio_browser.languages() if t.name == val
                    )
                if tags:
                    if len(tags) == 1 and (val := tags[0].get("value")):
                        kwargs["tag"] = val
                        kwargs["tag_exact"] = any(
                            True for t in await interaction.client.pylav.radio_browser.tags() if t.name == val
                        )
                    elif len(tags) > 1:
                        kwargs["tag_list"] = ",".join([tv for t in tags if (tv := t.get("value"))])

            if current:
                kwargs["name"] = current
            if not current:
                return [
                    Choice(
                        name=shorten_string(e.name, max_length=100)
                        if e.name
                        else shorten_string(max_length=100, string=_("Unnamed")),
                        value=f"{e.stationuuid}",
                    )
                    for e in await interaction.client.pylav.radio_browser.stations_by_votes(limit=25)
                ]
            if not kwargs:
                kwargs["limit"] = 1000
            stations = await interaction.client.pylav.radio_browser.search(**kwargs)

            async def _filter(c: Station):
                return (
                    await asyncio.to_thread(
                        fuzz.partial_ratio,
                        c.name,
                        current,
                    ),
                    c.votes,
                )

            extracted: list[Station] = await heapq.nlargest(asyncstdlib.iter(stations), n=25, key=_filter)

            return [
                Choice(
                    name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.stationuuid}"
                )
                for e in extracted
            ]

    class TagConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[Tag]:
            """Converts a Tag name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                return await ctx.pylav.radio_browser.tags(arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Tag with name `{arg}` not found").format(arg=arg)) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[Tag]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            tags = await interaction.client.pylav.radio_browser.tags()
            if not current:
                return [
                    Choice(
                        name=shorten_string(e.name, max_length=100)
                        if e.name
                        else shorten_string(max_length=100, string=_("Unnamed")),
                        value=f"{e.name}",
                    )
                    for e in tags
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(tags), n=25, key=_filter)

            return [
                Choice(
                    name=shorten_string(e.name, max_length=100)
                    if e.name
                    else shorten_string(max_length=100, string=_("Unnamed")),
                    value=f"{e.name}",
                )
                for e in extracted
            ]

    class LanguageConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[Language]:
            """Converts a Language name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                return await ctx.pylav.radio_browser.languages(arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Language with name `{arg}` not found").format(arg=arg)) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[Language]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            languages = await interaction.client.pylav.radio_browser.languages()
            if not current:
                return [
                    Choice(
                        name=shorten_string(e.name, max_length=100)
                        if e.name
                        else shorten_string(max_length=100, string=_("Unnamed")),
                        value=f"{e.name}",
                    )
                    for e in languages
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(languages), n=25, key=_filter)

            return [
                Choice(
                    name=shorten_string(e.name, max_length=100)
                    if e.name
                    else shorten_string(max_length=100, string=_("Unnamed")),
                    value=f"{e.name}",
                )
                for e in extracted
            ]

    class StateConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[State]:
            """Converts a State name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []
            try:
                return await ctx.pylav.radio_browser.states(state=arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("State with name `{arg}` not found")) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[State]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            data = interaction.data
            options = data.get("options", [])
            kwargs = {}
            if options:
                country = [v for v in options if v.get("name") == "country"]

                if country and (val := country[0].get("value")):
                    kwargs["country"] = val
            states = await interaction.client.pylav.radio_browser.states(**kwargs)
            if not current:
                return [
                    Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                    for e in states
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(states), n=25, key=_filter)

            return [
                Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                for e in extracted
            ]

    class CodecConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[Codec]:
            """Converts a Codec name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                return await ctx.pylav.radio_browser.codecs(arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Codec with name `{arg}` not found").format(arg=arg)) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[Codec]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            codecs = await interaction.client.pylav.radio_browser.codecs()
            if not current:
                return [
                    Choice(
                        name=shorten_string(e.name, max_length=100)
                        if e.name
                        else shorten_string(max_length=100, string=_("Unnamed")),
                        value=f"{e.name}",
                    )
                    for e in codecs
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(codecs), n=25, key=_filter)

            return [
                Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                for e in extracted
            ]

    class CountryCodeConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[CountryCode]:
            """Converts a CountryCode name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                return await ctx.pylav.radio_browser.countrycodes(arg)
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Country code `{arg}` not found").format(arg=arg)) from e

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[CountryCode]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            country_codes = await interaction.client.pylav.radio_browser.countrycodes()
            if not current:
                return [
                    Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                    for e in country_codes
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(country_codes), n=25, key=_filter)

            return [
                Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                for e in extracted
            ]

    class CountryConverter(Transformer):
        @classmethod
        async def convert(cls, ctx: DISCORD_CONTEXT_TYPE, arg: str) -> list[Country]:
            """Converts a Country name to to a matching object"""
            if ctx.bot.pylav.radio_browser.disabled:
                return []

            try:
                countries = await ctx.pylav.radio_browser.countries()
            except EntryNotFoundException as e:
                raise commands.BadArgument(_("Country with name `{arg}` not found").format(arg=arg)) from e

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, arg, c.name), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(countries), n=25, key=_filter)
            return extracted

        @classmethod
        async def transform(cls, interaction: DISCORD_INTERACTION_TYPE, argument: str) -> list[Country]:
            if not interaction.response.is_done():
                await interaction.response.defer(ephemeral=True)
            ctx = await interaction.client.get_context(interaction)
            if interaction.client.pylav.radio_browser.disabled:
                return []
            return await cls.convert(ctx, argument)

        @classmethod
        async def autocomplete(cls, interaction: DISCORD_INTERACTION_TYPE, current: str) -> list[Choice]:
            if interaction.client.pylav.radio_browser.disabled:
                return [
                    Choice(
                        name=shorten_string(max_length=100, string=_("Radio Browser is disabled")),
                        value="???",
                    )
                ]
            data = interaction.data
            options = data.get("options", [])
            kwargs = {}
            if options:
                code = [v for v in options if v.get("name") in ["countrycode", "code"]]
                if code and (val := code[0].get("value")):
                    kwargs["code"] = val
            countries = await interaction.client.pylav.radio_browser.countries(**kwargs)
            if not current:
                return [
                    Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                    for e in countries
                ][:25]

            async def _filter(c):
                return await asyncio.to_thread(fuzz.partial_ratio, c.name, current), [-ord(c) for c in c.name]

            extracted = await heapq.nlargest(asyncstdlib.iter(countries), n=25, key=_filter)

            return [
                Choice(name=shorten_string(e.name, max_length=100) if e.name else _("Unnamed"), value=f"{e.name}")
                for e in extracted
            ]
