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


ESTADOS_ACTIVIDAD = [
    (1, 'Activo'),
    (2, 'Reactivado'),
    (3, 'Suspendido'),
    (4, 'Latente'),
    (5, 'Abandonado'),
    (6, 'Estabilizado'),
    (7, 'Relicto')
]

ESTILOS_ACTIVIDAD = [
    (1, 'Complejo'),
    (2, 'Compuesto'),
    (3, 'Múltiple'),
    (4, 'Sucesivo'),
    (5, 'Único'),
    (6, 'Enjambre')
]

ESPACIAMIENTOS = [
    '>2', '2 - 0.6', '0.6 - 0.2', '0.2 - 0.06', '<0.06'
]
