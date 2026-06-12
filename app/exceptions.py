from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(response.data, dict) and 'detail' in response.data:
        response.data = {'error': response.data['detail']}
    else:
        response.data = {'errors': response.data}

    return response
