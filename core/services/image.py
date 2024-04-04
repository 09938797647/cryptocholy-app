import logging
import uuid
from io import BytesIO
from pathlib import Path

from telegram import Document, PhotoSize

from core.constants import MAX_ALLOWED_FILE_SIZE
from core.db import Base
from core.services.base import BaseService
from core.settings import Config


logger = logging.getLogger(__name__)


class FileValidationError(Exception):
    ...


class ImageService(BaseService):
    @staticmethod
    def _generate_relative_file_path(
        model_klass: type[Base], file_extension: str
    ) -> Path:
        for _ in range(5):
            file_name = (
                f"{model_klass.__name__}_{uuid.uuid4().hex}{file_extension}".lower()
            )
            if not (file_path := Config.STATIC_UPLOAD_PATH / file_name).exists():
                return file_path.relative_to(Config.STATIC_ROOT_PATH)

        raise NameError("Can't generate filename")

    def _get_target_object(self, model_klass: type[Base], entity_id: int) -> Base:
        obj = (
            self.db_session.query(model_klass).filter(model_klass.id == entity_id).one()
        )
        return obj

    def _delete_file(self, relative_file_path: str) -> None:
        ...

    @classmethod
    def validate_input_file(
        cls,
        attachment: Document | tuple[PhotoSize],
    ) -> Document | PhotoSize:
        if isinstance(attachment, tuple):
            effective_file = attachment[-1]
        else:
            effective_file = attachment

        logger.info(
            "Uploading a new image: %s, file size=%s",
            effective_file.file_id,
            effective_file.file_size,
        )

        if effective_file.file_size > MAX_ALLOWED_FILE_SIZE:
            raise FileValidationError(
                f"The file exceeds the maximum allowed size of {MAX_ALLOWED_FILE_SIZE / 1024 / 1024}Mb"
            )
        return effective_file

    def get_path(
        self, model_klass: type[Base], entity_id: int, attribute_name: str
    ) -> str | None:
        obj = self._get_target_object(model_klass, entity_id)
        current_value = getattr(obj, attribute_name)
        return current_value

    def save_image(
        self,
        model_klass: type[Base],
        entity_id: int,
        attribute_name: str,
        image: BytesIO,
        file_extension: str,
    ) -> Path:
        target_obj = self._get_target_object(model_klass, entity_id)

        new_relative_file_path = self._generate_relative_file_path(
            model_klass, file_extension=file_extension
        )
        # 1 - save new file
        with open(Config.STATIC_ROOT_PATH / new_relative_file_path, "wb") as file:
            file.write(image.getvalue())

        previous_file_name = getattr(target_obj, attribute_name)
        # 2 - update the path in the database
        setattr(target_obj, attribute_name, str(new_relative_file_path))
        self.db_session.add(target_obj)
        self.db_session.commit()
        # 3 - remove previous file from the database
        if previous_file_name:
            (Config.STATIC_ROOT_PATH / previous_file_name).unlink(missing_ok=True)

        return new_relative_file_path
