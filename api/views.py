from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json
import logging

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        challenge = request.query_params.get('challenge')
        logger.info(f"Challenge received: {challenge}")
        return HttpResponse(challenge or '', content_type='text/plain')

    def post(self, request, *args, **kwargs):
        logger.info("POST request object: %s", request)
        logger.info("Callback received: %s", request.data)

        return HttpResponse(
            "200 OK - Callback received successfully. Please respond with success message.",
            content_type='text/plain'
        )
