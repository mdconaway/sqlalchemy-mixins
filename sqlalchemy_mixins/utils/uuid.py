import uuid
from abc import ABC

from sqlalchemy.types import TypeDecorator, BINARY
from sqlalchemy.dialects.postgresql import UUID as psqlUUID


class UUID(TypeDecorator, ABC):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    BINARY(16), to store UUID.

    usage example:
    # uid = Column(UUID(), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)

    """
    impl = BINARY

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(psqlUUID())
        else:
            return dialect.type_descriptor(BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                if isinstance(value, bytes):
                    value = uuid.UUID(bytes=value)
                elif isinstance(value, int):
                    value = uuid.UUID(int=value)
                elif isinstance(value, str):
                    value = uuid.UUID(value)
        if dialect.name == 'postgresql':
            return str(value)
        else:
            return value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return uuid.UUID(value)
        else:
            return uuid.UUID(bytes=value)