from django import template
import json

register = template.Library()


class Data(object):
    @classmethod
    def to_dict(cls, obj):
        to_dict = getattr(obj, "to_dict", None)
        if callable(to_dict):
            return obj.to_dict()
        else:
            return obj.__dict__


    @classmethod
    def json_dumps(cls, data: list) -> str:
        return json.dumps(data, default=Data.to_dict, sort_keys=True, indent=4)


@register.simple_tag
def json_dumps(model_object: list) -> str:
    return Data.json_dumps(model_object)
