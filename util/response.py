import json

from django.http import HttpResponse


def response_message(success=False, data=None, **kwargs):
    allowed_keys = ('text', 'info', 'warning', 'error')
    return HttpResponse(
        json.dumps(
            {
                'success': success,
                'data': data,
                'message': {
                    k: v for k, v in kwargs.items() if k in allowed_keys
                    }
            }
        ), content_type='application/json'
    )
