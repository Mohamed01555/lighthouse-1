from abc import ABC


class BaseViewSet(ABC):
    def __init__(self, request):
        self.request = request
        self.verbs = {}

    def respond(self):
        method = self.verbs[self.request.method]
        response = method()
        return response
