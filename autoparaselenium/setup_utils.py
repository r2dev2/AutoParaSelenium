import os
import sys
import tarfile
from pathlib import Path
from typing import Callable, Dict, List
from zipfile import ZipFile

import requests

# delete 32 of win32 and linux32
platform = sys.platform.replace("32", "")


def download(url: str, location: Path) -> None:
    __touch(location)
    r = requests.get(url)
    r.raise_for_status()
    with open(location, "wb+") as fout:
        fout.write(r.content)


def unzip(source: str, dest_folder: str) -> None:
    with ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(dest_folder)


def untar(source: str, dest_folder: str) -> None:
    with tarfile.open(source) as tar_ref:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar_ref, dest_folder)


def __touch(location: Path) -> None:
    location.parent.mkdir(parents=True, exist_ok=True)
    location.touch()


def setup_driver(platform_install, platform_drivers, pwd: Path) -> None:
    if not Path(pwd / platform_drivers[platform]).exists():
        __download_and_extract(*platform_install[platform], pwd)

    # sometimes webdriver is nested in a folder after zip extraction
    if not Path(pwd / platform_drivers[platform]).exists():
        os.link(
            next(pwd.rglob(platform_drivers[platform])),
            pwd / platform_drivers[platform]
        )


def __download_and_extract(
    url: str, extract: Callable[[str, str], None], pwd: Path
) -> None:
    download(url, pwd / "temp")
    extract(pwd / "temp", pwd)
