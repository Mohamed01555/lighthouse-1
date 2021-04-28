from django.utils.deprecation import MiddlewareMixin


class FormDataParsingMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        supported_methods = ["PUT", "PATCH"]
        method = request.method
        if (
            request.content_type == "multipart/form-data"
            and method in supported_methods
        ):
            if hasattr(request, "_post"):
                del request._post
                del request._files
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = method
            except AttributeError as e:
                request.META["REQUEST_METHOD"] = "POST"
                request._load_post_and_files()
                request.META["REQUEST_METHOD"] = method

            setattr(request, method, request.POST)
