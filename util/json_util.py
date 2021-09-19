import json
import logging

log = logging.getLogger(__name__)

class JsonUtil:

    @classmethod
    def jsonify(cls, object, encoder, pretty_print=False):
        tabs = 4 if pretty_print else None
        json_str = json.dumps(
            obj=object, cls=encoder, indent=tabs
        )
        return json_str
