import os

import flet as ft

from frontend.runtime_config import PUBLIC_BACKEND_URL


# A packaged app runs on the user's device, where 127.0.0.1 is not the
# DigitalOcean server. Keep the public endpoint as the native default while
# still allowing development builds to override it.
os.environ.setdefault("CHATTER_BACKEND_URL", PUBLIC_BACKEND_URL)

from frontend.main import main  # noqa: E402


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
