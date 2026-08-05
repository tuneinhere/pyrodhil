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

import re
from pathlib import Path
from sys import argv

from setuptools import setup, find_packages


BUILD_COMMANDS = {"bdist_wheel", "install", "develop"}


def is_build_command() -> bool:
    return any(arg in BUILD_COMMANDS for arg in argv[1:])


def raw_api_is_complete() -> bool:
    """
    Check whether generated raw API files already exist.

    If these files are complete, we skip the API compiler so pip install
    won't overwrite pyrogram/raw/all.py and other generated raw files.
    """
    required_files = [
        Path("pyrogram/raw/all.py"),
        Path("pyrogram/raw/base/keyboard_button_style.py"),
        Path("pyrogram/raw/types/keyboard_button_style.py"),
        Path("pyrogram/raw/types/keyboard_button_callback.py"),
        Path("pyrogram/raw/types/keyboard_button.py"),
    ]

    if not all(path.exists() for path in required_files):
        return False

    all_py = Path("pyrogram/raw/all.py").read_text(encoding="utf-8")

    required_markers = [
        "0x4fdd3430",  # KeyboardButtonStyle
        "0xe62bc960",  # New KeyboardButtonCallback with style
    ]

    return all(marker in all_py for marker in required_markers)


def errors_api_is_complete() -> bool:
    """
    Check whether generated RPC error files already exist.
    """
    return (
        Path("pyrogram/errors/exceptions").exists()
        and Path("pyrogram/errors/exceptions/__init__.py").exists()
    )


def ensure_raw_compat_aliases() -> None:
    """
    pyrogram/raw/all.py is generated and can be overwritten by the compiler.

    This function safely restores compatibility aliases after optional
    raw generation.

    Important:
    - 0x35bbdb6b is the legacy KeyboardButtonCallback constructor.
    - 0xe62bc960 is the new KeyboardButtonCallback constructor.
    - 0x4fdd3430 is KeyboardButtonStyle.
    """
    all_py_path = Path("pyrogram/raw/all.py")

    if not all_py_path.exists():
        return

    text = all_py_path.read_text(encoding="utf-8")

    aliases = []

    if Path("pyrogram/raw/types/keyboard_button_callback.py").exists():
        aliases.append(
            '    0x35bbdb6b: "pyrogram.raw.types.KeyboardButtonCallback",\n'
        )

    if Path("pyrogram/raw/types/keyboard_button_style.py").exists():
        aliases.append(
            '    0x4fdd3430: "pyrogram.raw.types.KeyboardButtonStyle",\n'
        )

    changed = False

    for alias in aliases:
        constructor_id = alias.strip().split(":", 1)[0]

        if constructor_id not in text:
            text = text.replace("objects = {\n", "objects = {\n" + alias, 1)
            changed = True

    if changed:
        all_py_path.write_text(text, encoding="utf-8")


with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r if i.strip()]

with open("pyrogram/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()


if is_build_command():
    if raw_api_is_complete():
        print("Raw API already exists and is complete, skipping API compiler.")
    else:
        print("Raw API is missing/incomplete, running API compiler.")
        from compiler.api import compiler as api_compiler

        api_compiler.start()

    ensure_raw_compat_aliases()

    if errors_api_is_complete():
        print("Errors API already exists, skipping errors compiler.")
    else:
        print("Errors API is missing/incomplete, running errors compiler.")
        from compiler.errors import compiler as errors_compiler

        errors_compiler.start()


setup(
    name="levigram",
    version=version,
    description="Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots (Navy Fork)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/plerbanget/pyrogram-new",
    download_url="https://github.com/plerbanget/pyrogram-new/releases/latest",
    author="Levine",
    author_email="gwangy682@gmail.com",
    license="LGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="telegram chat messenger mtproto api client library python",
    python_requires=">=3.8",
    package_data={
        "kelragram": ["py.typed"],
    },
    packages=find_packages(exclude=["compiler*", "tests*"]),
    zip_safe=False,
    install_requires=requires,
)
