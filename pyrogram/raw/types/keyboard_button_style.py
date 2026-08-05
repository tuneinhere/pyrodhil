from io import BytesIO
from typing import Optional, Any

from pyrogram.raw.core.primitives import Int, Long
from pyrogram.raw.core import TLObject


class KeyboardButtonStyle(TLObject):  # type: ignore
    __slots__ = ["bg_primary", "bg_danger", "bg_success", "icon"]

    ID = 0x4fdd3430
    QUALNAME = "types.KeyboardButtonStyle"

    def __init__(
        self,
        *,
        bg_primary: Optional[bool] = None,
        bg_danger: Optional[bool] = None,
        bg_success: Optional[bool] = None,
        icon: Optional[int] = None
    ) -> None:
        self.bg_primary = bg_primary
        self.bg_danger = bg_danger
        self.bg_success = bg_success
        self.icon = icon

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonStyle":
        flags = Int.read(b)

        bg_primary = True if flags & (1 << 0) else None
        bg_danger = True if flags & (1 << 1) else None
        bg_success = True if flags & (1 << 2) else None
        icon = Long.read(b) if flags & (1 << 3) else None

        return KeyboardButtonStyle(
            bg_primary=bg_primary,
            bg_danger=bg_danger,
            bg_success=bg_success,
            icon=icon
        )

    def write(self, *args: Any) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.bg_primary else 0
        flags |= (1 << 1) if self.bg_danger else 0
        flags |= (1 << 2) if self.bg_success else 0
        flags |= (1 << 3) if self.icon is not None else 0

        b.write(Int(flags))

        if self.icon is not None:
            b.write(Long(self.icon))

        return b.getvalue()
