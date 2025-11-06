from django import template
import json

register = template.Library()


class Data(object):

    @classmethod
    def json_dumps(cls, data: list) -> str:
        return json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@register.simple_tag
def json_dumps(model_object: list) -> str:
    return Data.json_dumps(model_object)
