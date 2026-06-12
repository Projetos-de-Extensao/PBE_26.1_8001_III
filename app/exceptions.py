from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if isinstance(response.data, dict) and 'detail' in response.data:
        response.data = {'error': response.data['detail']}
    elif isinstance(response.data, list) and len(response.data) == 1:
        response.data = {'error': response.data[0]}
    else:
        response.data = {'errors': response.data}

    return response
