#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from pyrogram import raw, types, enums
from ..object import Object


def resolve_button_style(style):
    if isinstance(style, enums.ButtonStyle):
        return style

    if style is None:
        return enums.ButtonStyle.DEFAULT

    return {
        "DEFAULT": enums.ButtonStyle.DEFAULT,
        "PRIMARY": enums.ButtonStyle.PRIMARY,
        "DANGER": enums.ButtonStyle.DANGER,
        "SUCCESS": enums.ButtonStyle.SUCCESS,
    }.get(str(style).upper(), enums.ButtonStyle.DEFAULT)


def resolve_icon_custom_emoji_id(icon_custom_emoji_id):
    if icon_custom_emoji_id is None:
        return None

    if icon_custom_emoji_id == "":
        return None

    return str(icon_custom_emoji_id)


def parse_icon_custom_emoji_id(icon_custom_emoji_id):
    if not icon_custom_emoji_id:
        return None

    try:
        return int(icon_custom_emoji_id)
    except (TypeError, ValueError):
        return None


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

        icon_custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown before the text of the button.

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Style of the button.
    """

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        web_app: "types.WebAppInfo" = None,
        icon_custom_emoji_id: Optional[str] = None,
        style: "enums.ButtonStyle" = enums.ButtonStyle.DEFAULT,
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app
        self.icon_custom_emoji_id = resolve_icon_custom_emoji_id(icon_custom_emoji_id)
        self.style = resolve_button_style(style)

    @staticmethod
    def read(b):
        button_style = enums.ButtonStyle.DEFAULT
        icon_custom_emoji_id = None

        raw_style = getattr(b, "style", None)

        if raw_style is not None:
            if getattr(raw_style, "bg_primary", False):
                button_style = enums.ButtonStyle.PRIMARY
            elif getattr(raw_style, "bg_danger", False):
                button_style = enums.ButtonStyle.DANGER
            elif getattr(raw_style, "bg_success", False):
                button_style = enums.ButtonStyle.SUCCESS

            raw_icon = getattr(raw_style, "icon", None)
            if raw_icon is not None:
                icon_custom_emoji_id = str(raw_icon)

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id,
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id,
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(url=b.url),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id,
            )

        return KeyboardButton(
            text=b.text,
            style=button_style,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    def write(self):
        kwargs = {}

        icon_id = parse_icon_custom_emoji_id(self.icon_custom_emoji_id)

        if (
            hasattr(raw.types, "KeyboardButtonStyle")
            and (
                self.style != enums.ButtonStyle.DEFAULT
                or icon_id is not None
            )
        ):
            kwargs["style"] = raw.types.KeyboardButtonStyle(
                bg_primary=self.style == enums.ButtonStyle.PRIMARY,
                bg_danger=self.style == enums.ButtonStyle.DANGER,
                bg_success=self.style == enums.ButtonStyle.SUCCESS,
                icon=icon_id,
            )

        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text, **kwargs)

        if self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text, **kwargs)

        if self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(
                text=self.text,
                url=self.web_app.url,
                **kwargs,
            )

        return raw.types.KeyboardButton(text=self.text, **kwargs)