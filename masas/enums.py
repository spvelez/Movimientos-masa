from enum import Enum


class UserRole(Enum):
    admin = (1, 'Administrador')
    user = (2, 'Geólogo')

    @classmethod
    def from_value(cls, value):
        for i in cls:
            if i.value[0] == value:
                return i

        return None
