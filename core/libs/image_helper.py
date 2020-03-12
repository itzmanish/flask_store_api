import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet('images', IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes FileStorage and save it to a folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Takes image name and folder and return it's full path"""
    return IMAGE_SET.path(filename, folder)


def find_images_any_format(filename: str = None, folder: str = None) -> Union[str, None]:
    """Takes a filename and return an image of any of the accepted format"""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = get_path(image, folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Takes FileStorage and return the file name
    Allow our function to call with file string and FileStorage both.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check for regex and return whether the string matches or not"""
    filename = _retrieve_filename(file)

    allowed_formats = "|".join(IMAGES)  # png|jpg|jpe|svg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_formats})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """
    Return full path of image in the path
    get_basename('some/folder/image.jpg') return 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """Returns file extension"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
