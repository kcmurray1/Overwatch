from flask.views import MethodView
from flask import current_app, request
from app.core.errors import APIError, response_template


class DockerEvents(MethodView):
    def post(self):
        payload = request.get_json()

        if not payload:
            raise APIError("Invalid event", payload)
        

        print(payload)

        return response_template(status=200, message="ok")