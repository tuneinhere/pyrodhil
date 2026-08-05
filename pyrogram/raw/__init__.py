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

from importlib import import_module

from . import types, functions, base, core
from .all import objects


for k, v in objects.items():
    path, name = v.rsplit(".", 1)
    objects[k] = getattr(import_module(path), name)

# Compatibility readers for legacy keyboard button constructors.
# Some old constructors do not have new style flags, so they must not be parsed
# directly by the new generated classes.

try:
    from io import BytesIO

    from .core import TLObject
    from .core.primitives import Int, Long, String, Bytes

    class _LegacyKeyboardButton:
        @staticmethod
        def read(b: BytesIO, *args):
            return types.KeyboardButton(text=String.read(b))

    class _LegacyKeyboardButtonUrl:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            url = String.read(b)
            return types.KeyboardButtonUrl(text=text, url=url)

    class _LegacyKeyboardButtonCallback:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            data = Bytes.read(b)
            return types.KeyboardButtonCallback(text=text, data=data)

    class _LegacyKeyboardButtonRequestPhone:
        @staticmethod
        def read(b: BytesIO, *args):
            return types.KeyboardButtonRequestPhone(text=String.read(b))

    class _LegacyKeyboardButtonRequestGeoLocation:
        @staticmethod
        def read(b: BytesIO, *args):
            return types.KeyboardButtonRequestGeoLocation(text=String.read(b))

    class _LegacyKeyboardButtonSwitchInline:
        @staticmethod
        def read(b: BytesIO, *args):
            flags = Int.read(b)
            same_peer = True if flags & (1 << 0) else None
            text = String.read(b)
            query = String.read(b)
            return types.KeyboardButtonSwitchInline(
                text=text,
                query=query,
                same_peer=same_peer,
            )

    class _LegacyKeyboardButtonGame:
        @staticmethod
        def read(b: BytesIO, *args):
            return types.KeyboardButtonGame(text=String.read(b))

    class _LegacyKeyboardButtonBuy:
        @staticmethod
        def read(b: BytesIO, *args):
            return types.KeyboardButtonBuy(text=String.read(b))

    class _LegacyKeyboardButtonUrlAuth:
        @staticmethod
        def read(b: BytesIO, *args):
            flags = Int.read(b)
            text = String.read(b)
            fwd_text = String.read(b) if flags & (1 << 0) else None
            url = String.read(b)
            button_id = Int.read(b)

            return types.KeyboardButtonUrlAuth(
                text=text,
                url=url,
                button_id=button_id,
                fwd_text=fwd_text,
            )

    class _LegacyKeyboardButtonRequestPoll:
        @staticmethod
        def read(b: BytesIO, *args):
            flags = Int.read(b)
            quiz = TLObject.read(b) if flags & (1 << 0) else None
            text = String.read(b)

            return types.KeyboardButtonRequestPoll(
                text=text,
                quiz=quiz,
            )

    class _LegacyKeyboardButtonUserProfile:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            user_id = Long.read(b)
            return types.KeyboardButtonUserProfile(text=text, user_id=user_id)

    class _LegacyKeyboardButtonWebView:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            url = String.read(b)
            return types.KeyboardButtonWebView(text=text, url=url)

    class _LegacyKeyboardButtonSimpleWebView:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            url = String.read(b)
            return types.KeyboardButtonSimpleWebView(text=text, url=url)

    class _LegacyKeyboardButtonRequestPeer:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            button_id = Int.read(b)
            peer_type = TLObject.read(b)
            max_quantity = Int.read(b)

            return types.KeyboardButtonRequestPeer(
                text=text,
                button_id=button_id,
                peer_type=peer_type,
                max_quantity=max_quantity,
            )

    class _LegacyKeyboardButtonCopy:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            copy_text = String.read(b)
            return types.KeyboardButtonCopy(text=text, copy_text=copy_text)

    # Legacy keyboard constructors without new style flags.
    objects[0xa2fa4880] = _LegacyKeyboardButton
    objects[0x258aff05] = _LegacyKeyboardButtonUrl
    objects[0x683a5e46] = _LegacyKeyboardButtonCallback
    objects[0xb16a6c29] = _LegacyKeyboardButtonRequestPhone
    objects[0xfc796b3f] = _LegacyKeyboardButtonRequestGeoLocation
    objects[0x93b9fbb5] = _LegacyKeyboardButtonSwitchInline
    objects[0x0568a748] = _LegacyKeyboardButtonSwitchInline
    objects[0x50f41ccf] = _LegacyKeyboardButtonGame
    objects[0xafd93fbb] = _LegacyKeyboardButtonBuy
    objects[0x10b78d29] = _LegacyKeyboardButtonUrlAuth
    objects[0xbbc7515d] = _LegacyKeyboardButtonRequestPoll
    objects[0x308660c1] = _LegacyKeyboardButtonUserProfile
    objects[0x13767230] = _LegacyKeyboardButtonWebView
    objects[0xa0c0505c] = _LegacyKeyboardButtonSimpleWebView
    objects[0x53d7bfd8] = _LegacyKeyboardButtonRequestPeer
    objects[0x75d2698e] = _LegacyKeyboardButtonCopy

    # Old callback constructor that already has flags in newer old layers.
    if hasattr(types, "KeyboardButtonCallback"):
        objects[0x35bbdb6b] = types.KeyboardButtonCallback

    # ButtonStyle constructor.
    if hasattr(types, "KeyboardButtonStyle"):
        objects[0x4fdd3430] = types.KeyboardButtonStyle

except Exception:
    pass
