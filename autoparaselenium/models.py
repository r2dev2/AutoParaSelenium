from pathlib import Path
from typing import List, Optional


class Extension:
    def __init__(self, *_, firefox: Optional[str] = None, chrome: Optional[str] = None):
        self.firefox = firefox
        self.chrome = chrome


class Conf:
    def __init__(
        self,
        *_,
        extensions: List[Extension] = [],
        headless=True,
        selenium_dir="drivers",
    ):
        self.extensions = extensions
        self.headless = headless
        self.selenium_dir = Path(selenium_dir)
