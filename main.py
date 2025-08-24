from z8ter.core import Z8ter
from z8ter.config import build_config

config = build_config(".env")


def create_app() -> Z8ter:
    app = Z8ter(
        debug=False,
        mode=config.get('Z8_MODE', default="dev")
        )
    return app


if __name__ == "__main__":
    app = create_app()
