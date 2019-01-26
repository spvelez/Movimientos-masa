from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey,
    Integer, Numeric, String, Text)
from sqlalchemy.orm import relationship
from masas.database import DbModel


class Movimiento(DbModel):
    __tablename__ = 'movimiento'

    id = Column(Integer, primary_key=True)

    encuestador = Column(String(128))
    fecha = Column(DateTime)
    institucion = Column(String(128))
    codigo = Column(String(128))

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
    espaciamiento = Column(String(8))

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
    humedad_uno = Column(String(2))

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

    dif_corona_punta = Column(Numeric(precision=2))
    long_corona_punta = Column(Numeric(precision=2))
    fahrboschung = Column(Numeric(precision=2))
    pre_falla = Column(Numeric(precision=2))
    post_falla = Column(Numeric(precision=2))
    direccion = Column(String(16))
    azimut = Column(Numeric(precision=2))

    profundidad_falla = Column(Numeric(precision=2))
    ancho_falla = Column(Numeric(precision=2))
    longitud_falla = Column(Numeric(precision=2))
    espesor_masa = Column(Numeric(precision=2))
    ancho_masa = Column(Numeric(precision=2))
    longitud_masa = Column(Numeric(precision=2))
    longitud_total = Column(Numeric(precision=2))
    volumen_inicial = Column(Numeric(precision=2))
    volumen_desplazado = Column(Numeric(precision=2))
    area_inicial = Column(Numeric(precision=2))
    area_total = Column(Numeric(precision=2))
    distancia_viaje = Column(Numeric(precision=2))
    runup = Column(Numeric(precision=2))

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
    distancia_sismo = Column(Numeric(precision=2))
    magnitud_sismo = Column(Numeric(precision=2))
    profundidad_sismo = Column(Numeric(precision=2))

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
    agricula = Column(Integer)
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

    tipo = Column(String(2))
    longitud_presa = Column(Numeric(precision=2))
    altura = Column(Numeric(precision=2))
    ancho = Column(Numeric(precision=2))
    talud_arriba = Column(Numeric(precision=2))
    talud_abajo = Column(Numeric(precision=2))
    volumen_presa = Column(Numeric(precision=2))

    corona = Column(Boolean)
    filtracion = Column(Boolean)
    tubificacion_natural = Column(Boolean)
    obstruccion = Column(Boolean)
    erosion = Column(Boolean)
    estabilizacion = Column(Boolean)
    tubificacion_artificial = Column(Boolean)

    socavada_ligera = Column(Boolean)
    socavada_moderada = Column(Boolean)
    socavada_fuerte = Column(Boolean)
    socavada_completa = Column(Boolean)
    parc_fallada = Column(Boolean)
    fallada = Column(Boolean)
    llenandose = Column(Boolean)

    longitud_embalse = Column(Numeric(precision=2))
    area_embalse = Column(Numeric(precision=2))
    volumen_embalse = Column(Numeric(precision=2))
    nivel_agua_corona = Column(Numeric(precision=2))
    area_cuenca = Column(Numeric(precision=2))
    caudal_entrada = Column(Numeric(precision=2))
    caudal_salida = Column(Numeric(precision=2))
    tasa_llenado = Column(Numeric(precision=2))

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
    valor = Column(Numeric(precision=2))

    danio_id = Column(Integer, ForeignKey('dano.id'))
