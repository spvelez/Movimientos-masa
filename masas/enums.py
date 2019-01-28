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

TIPOS_MOVIMIENTO = [
    ('C', 'Caída'),
    ('V', 'Volcamiento'),
    ('DR', 'Deslizamiento rotacional'),
    ('DT', 'Deslizamiento traslacional'),
    ('PL', 'Propagación lateral'),
    ('R', 'Reptación'),
    ('F', 'Flujo'),
    ('DGP', 'Deformaciones grav. profundas')
]

HUMEDADES = [
    ('S', 'Seco'),
    ('LH', 'Lig. húmedo'),
    ('H', 'Húmedo'),
    ('MH', 'Muy húmedo'),
    ('MJ', 'Mojado')
]

PLASTICIDADES = [
    ('A', 'Alta'),
    ('M', 'Media'),
    ('B', 'Baja'),
    ('NP', 'No plástico'),
]

ORIGENES_SUELO = [
    ('R', 'Residual'),
    ('S', 'Sedimentario')
]

VELOCIDADES = [
    ('EXTR', 'Extra rápido'),
    ('MUYR', 'Muy rápido'),
    ('RAP', 'Rápido'),
    ('MOD', 'Moderado'),
    ('LEN', 'Lento'),
    ('MUYL', 'Muy lento'),
    ('EXTL', 'Extra lento'),
]

MODOS_MORFM = [
    ('O', 'Ondulación'),
    ('E', 'Escalonamiento')
]

SEVERIDADES_MORFM = [
    ('L', 'Leve'),
    ('L', 'Media'),
    ('L', 'Severa'),
]

CAUSAS_MOV = [
    ('C', 'Causante'),
    ('D', 'Detonante')
]

CONDICIONES_PRESA = [
    ('CORREB', 'Corona rebosada'),
    ('FILTRA', 'Filtración'),
    ('TUBNAT', 'Tubificación natural'),
    ('OBSPAR', 'Obstrucción parcial'),
    ('ERPATA', 'Erosión de la pata'),
    ('ESTART', 'Estabilización artificial'),
    ('TUBART', 'Tubificación artificial'),
    ('LIGSOC', 'Ligeramente socavada'),
    ('MODSOC', 'Moderadamente socavada'),
    ('FUESOC', 'Fuertemente socavada'),
    ('COMSOC', 'Completamente socavada'),
    ('PARFAL', 'Parcialmente fallada'),
    ('FALLA', 'Fallada'),
    ('LLENA', 'Llenándose'),
]

ORIGENES_DANO = [
    ('INF', 'Infraestrutura'),
    ('AE', 'Actividades económicas'),
    ('DA', 'Daños ambientales')
]

INTENSIDADES_DANO = [
    ('DL', 'Daño leve'),
    ('DM', 'Daño moderado'),
    ('DS', 'Daño severo'),
    ('DT', 'Destrucción total')
]
