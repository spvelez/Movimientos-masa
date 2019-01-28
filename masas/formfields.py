from wtforms import (
    FieldList, DecimalField, HiddenField, IntegerField, RadioField)


class IdField(HiddenField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = int(valuelist[0])
        else:
            self.data = None


class NullableIntegerField(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            super(NullableIntegerField, self).process_formdata(valuelist)
        else:
            self.data = None


class NullableDecimalField(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            super(NullableDecimalField, self).process_formdata(valuelist)
        else:
            self.data = None


class OptionalRadioField(RadioField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            super(OptionalRadioField, self).process_formdata(valuelist)
        else:
            self.data = None

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break


class CustomFieldList(FieldList):
    def __init__(self, unbound_field, obj_ctor, label=None, validators=None,
                 min_entries=0, max_entries=None, default=tuple(), **kwargs):

        super(CustomFieldList, self).__init__(unbound_field, label,
                                              validators, min_entries,
                                              max_entries, default, **kwargs)

        self.obj_ctor = obj_ctor

    def populate_obj(self, obj, name):
        values = getattr(obj, name, None)

        self.prepare_list(values)
        super(CustomFieldList, self).populate_obj(obj, name)

    def prepare_list(self, obj_list):
        # eliminar los objetos que no están en el formulario
        for obj in obj_list:
            exists = any(fields['id'].data == obj.id for fields in self)

            if not exists:
                obj_list.remove(obj)

        # insertar los elementos agregados en el formulario en el mismo orden
        i = 0
        for fields in self:
            # los nuevos elementos no tienen id
            if not fields['id'].data:
                obj_list.insert(i, self.obj_ctor())

            i = i + 1
