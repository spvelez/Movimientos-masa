from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey,
    Integer, Float, String, Text)
from sqlalchemy.orm import relationship, reconstructor
from masas.core.database import DbModel


class Movimiento(DbModel):
    __tablename__ = 'movimiento'

    id = Column(Integer, primary_key=True)

    encuestador = Column(String(128))
    fecha = Column(DateTime)
    institucion = Column(String(128))
    codigo = Column(String(128))

    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship('User')

    localizacion = relationship('Localizacion', uselist=False)
    actividad = relationship('Actividad', uselist=False)
    litologia = relationship('Litologia', uselist=False)
    clasificacion = relationship('Clasificacion', uselist=False)
    morfometria = relationship('Morfometria', uselist=False)
    causa = relationship('Causa', uselist=False)
    cobertura_suelo = relationship('CoberturaSuelo', uselist=False)
    uso_suelo = relationship('UsoSuelo', uselist=False)
    documentos_ref = relationship('DocumentoReferencia', backref='movimiento')
    efecto_secundario = relationship('EfectoSecundario', uselist=False)
    dano = relationship('Dano', uselist=False)

    def __init__(self):
        self._observers = set()

    @reconstructor
    def init_on_load(self):
        self._observers = set()

    def suscribe(self, observer):
        observer.publisher = self
        self._observers.add(observer)

    def unsuscribe(self, observer):
        observer.publisher = None
        self._observers.discard(observer)

    def notify(self, author):
        for o in self._observers:
            o.update(author)


class Localizacion(DbModel):
    __tablename__ = 'localizacion'

    id = Column(Integer, primary_key=True)

    pais = Column(String(128))
    provincia = Column(String(128))
    ciudad = Column(String(128))
    localidad = Column(String(128))

    sitio = Column(String(128))
    norte = Column(Integer)
    este = Column(Integer)
    proyeccion = Column(String(128))
    altura = Column(Integer)

    ref_geograficos = Column(Text)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))

    mapas = relationship('Mapa', backref='localizacion')
    fotos = relationship('Foto', backref='localizacion')


class Mapa(DbModel):
    __tablename__ = 'mapa'

    id = Column(Integer, primary_key=True)

    nro_mapa = Column(String(128))
    anio = Column(String(4))
    escala = Column(String(128))
    editor = Column(String(128))

    localizacion_id = Column(Integer, ForeignKey('localizacion.id'))


class Foto(DbModel):
    __tablename__ = 'foto'

    id = Column(Integer, primary_key=True)

    nro_foto = Column(String(128))
    anio = Column(String(4))
    escala = Column(String(128))
    editor = Column(String(128))

    localizacion_id = Column(Integer, ForeignKey('localizacion.id'))


class Actividad(DbModel):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True)

    primera_fecha = Column(DateTime)
    ultima_fecha = Column(DateTime)

    edad = Column(String(4))
    estado = Column(Integer)
    estilo = Column(Integer)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))

    distribucion = relationship('Distribucion', uselist=False)


class Distribucion(DbModel):
    __tablename__ = 'distribucion'

    id = Column(Integer, primary_key=True)

    retrogresivo = Column(Boolean)
    avanzado = Column(Boolean)
    ensanchado = Column(Boolean)
    confinado = Column(Boolean)
    creciente = Column(Boolean)
    decreciente = Column(Boolean)
    movil = Column(Boolean)

    actividad_id = Column(Integer, ForeignKey('actividad.id'))


class Litologia(DbModel):
    __tablename__ = 'litologia'

    id = Column(Integer, primary_key=True)

    descripcion = Column(Text)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))

    detalles = relationship('DetalleLitologia', backref='litologia')


class DetalleLitologia(DbModel):
    __tablename__ = 'detalle_litologia'

    id = Column(Integer, primary_key=True)

    estructura = Column(String(128))
    dir_buzamiento = Column(String(64))
    buzamiento = Column(String(64))
    espaciamiento = Column(String(10))

    litologia_id = Column(Integer, ForeignKey('litologia.id'))


class Clasificacion(DbModel):
    __tablename__ = 'clasificacion'

    id = Column(Integer, primary_key=True)

    sistema = Column(String(128))
    nombre = Column(String(128))

    tipo_uno = Column(String(4))
    tipo_dos = Column(String(4))

    roca_uno = Column(Integer)
    roca_dos = Column(Integer)
    detritos_uno = Column(Integer)
    detritos_dos = Column(Integer)
    tierra_uno = Column(Integer)
    tierra_dos = Column(Integer)

    bloques_uno = Column(Integer)
    bloques_dos = Column(Integer)
    cantos_uno = Column(Integer)
    cantos_dos = Column(Integer)
    grava_uno = Column(Integer)
    grava_dos = Column(Integer)
    arena_uno = Column(Integer)
    arena_dos = Column(Integer)
    finos_uno = Column(Integer)
    finos_dos = Column(Integer)
    organica_uno = Column(Integer)
    organica_dos = Column(Integer)

    humedad_uno = Column(String(2))
    humedad_dos = Column(String(2))

    plasticidad_uno = Column(String(2))
    plasticidad_dos = Column(String(2))

    origen = Column(String(1))

    uscs = Column(Text)

    canalizado = Column(Boolean)
    no_canalizado = Column(Boolean)
    licuacion = Column(Boolean)
    otra_caracteristica = Column(String(128))

    velocidad = Column(String(4))
    vmax = Column(String(64))
    vmedia = Column(String(64))

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class Morfometria(DbModel):
    __tablename__ = 'morfometria'

    id = Column(Integer, primary_key=True)

    dif_corona_punta = Column(Float())
    long_corona_punta = Column(Float())
    fahrboschung = Column(Float())
    pre_falla = Column(Float())
    post_falla = Column(Float())
    direccion = Column(String(16))
    azimut = Column(Float())

    profundidad_falla = Column(Float())
    ancho_falla = Column(Float())
    longitud_falla = Column(Float())
    espesor_masa = Column(Float())
    ancho_masa = Column(Float())
    longitud_masa = Column(Float())
    longitud_total = Column(Float())
    volumen_inicial = Column(Float())
    volumen_desplazado = Column(Float())
    area_inicial = Column(Float())
    area_total = Column(Float())
    distancia_viaje = Column(Float())
    runup = Column(Float())

    modo = Column(String(1))
    severidad = Column(String(1))

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class Causa(DbModel):
    __tablename__ = 'causa'

    id = Column(Integer, primary_key=True)

    material_debil = Column(Boolean)
    material_sensitivo = Column(Boolean)
    material_colapsible = Column(Boolean)
    material_meteor_fisica = Column(Boolean)
    material_meteor_quimica = Column(Boolean)
    material_corte = Column(Boolean)
    material_fisurado = Column(Boolean)
    orient_desfavorable = Column(Boolean)
    contraste_perm = Column(Boolean)
    constraste_rigidez = Column(Boolean)
    meteor_congelamiento = Column(Boolean)
    meteor_expansion = Column(Boolean)
    deforestacion = Column(Boolean)

    mov_tectonico = Column(String(1))
    sismo = Column(String(1))
    magnitud_sismo = Column(String(32))
    escala_sismo = Column(String(32))
    distancia_sismo = Column(Float())
    profundidad_sismo = Column(Float())

    erupcion = Column(String(1))
    lluvias = Column(String(1))
    viento = Column(String(1))
    deshielo = Column(String(1))
    glaciares = Column(String(1))
    romp_lagos = Column(String(1))
    romp_presas = Column(String(1))
    desembalse = Column(String(1))
    embalse = Column(String(1))
    erosion_glaciares = Column(String(1))
    erosion_superficial = Column(String(1))

    soc_corriente_agua = Column(String(1))
    soc_oleaje = Column(String(1))
    excavacion_talud = Column(String(1))
    carga_corona = Column(String(1))
    erosion_subterranea = Column(String(1))
    irrigacion = Column(String(1))
    mant_sistema_drenaje = Column(String(1))
    escapes_tuberias = Column(String(1))
    mineria = Column(String(1))
    disp_esteriles_escombros = Column(String(1))
    vibracion_artificial = Column(String(1))
    otros = Column(String(1))

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class CoberturaSuelo(DbModel):
    __tablename__ = 'cobertura_suelo'

    id = Column(Integer, primary_key=True)

    herbacea = Column(Integer)
    bosque_selva = Column(Integer)
    matorrales = Column(Integer)
    cuerpo_agua = Column(Integer)
    cultivos = Column(Integer)
    construcciones = Column(Integer)
    sin_cobertura = Column(Integer)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class UsoSuelo(DbModel):
    __tablename__ = 'uso_suelo'

    id = Column(Integer, primary_key=True)

    ganaderia = Column(Integer)
    area_protegida = Column(Integer)
    agricola = Column(Integer)
    recreacion = Column(Integer)
    arqueologica = Column(Integer)
    industrial = Column(Integer)
    vivienda = Column(Integer)
    vias = Column(Integer)
    mineria = Column(Integer)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class DocumentoReferencia(DbModel):
    __tablename__ = 'documento_referencia'

    id = Column(Integer, primary_key=True)

    autores = Column(String(256))
    anio = Column(String(4))
    titulo = Column(String(128))
    libro = Column(String(128))
    editor = Column(String(128))
    ciudad = Column(String(128))
    paginas = Column(String(5))

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class EfectoSecundario(DbModel):
    __tablename__ = 'efecto_secundario'

    id = Column(Integer, primary_key=True)

    tipo = Column(String(3))
    longitud_presa = Column(Float())
    altura = Column(Float())
    ancho = Column(Float())
    talud_arriba = Column(Float())
    talud_abajo = Column(Float())
    volumen_presa = Column(Float())

    condicion_presa = Column(String(6))

    longitud_embalse = Column(Float())
    area_embalse = Column(Float())
    volumen_embalse = Column(Float())
    nivel_agua_corona = Column(Float())
    area_cuenca = Column(Float())
    caudal_entrada = Column(Float())
    caudal_salida = Column(Float())
    tasa_llenado = Column(Float())

    tsunami = Column(Boolean)
    empalizada = Column(Boolean)
    sedimentacion = Column(Boolean)
    sismo = Column(Boolean)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))


class Dano(DbModel):
    __tablename__ = 'dano'

    id = Column(Integer, primary_key=True)

    muertos = Column(Integer)
    heridos = Column(Integer)
    damnificados = Column(Integer)

    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))

    detalles = relationship('DetalleDano', backref='dano')


class DetalleDano(DbModel):
    __tablename__ = 'detalle_dano'

    id = Column(Integer, primary_key=True)
    origen = Column(String(3))
    tipo = Column(String(128))
    unidad = Column(String(128))
    intensidad = Column(String(2))
    valor = Column(Float())

    danio_id = Column(Integer, ForeignKey('dano.id'))
