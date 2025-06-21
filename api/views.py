from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CallbackView(APIView):
    authentication_classes = [] # No se requiere autenticación para este endpoint
    permission_classes = []     # No se requieren permisos
    print("ok")
    def get(self, request, *args, **kwargs):
        """
        Maneja las peticiones GET a /callback.
        Devuelve el valor del parámetro 'challenge' como texto plano.
        """
        challenge = request.query_params.get('challenge', 'DeliverArPwd2025!')
        # El otro parámetro 'code' que mencionaste también se accedería así:
        # code = request.query_params.get('code', '')
        # Devolvemos el challenge como texto plano
        # DRF por defecto intenta renderizar a JSON, para texto plano hay que especificarlo
        return Response(challenge, content_type='text/plain')

    def post(self, request, *args, **kwargs):
        """
        Maneja las peticiones POST a /callback.
        Aquí procesarías la información enviada en el cuerpo de la petición.
        """
        # Acceder a los datos del cuerpo de la petición POST:
        # data = request.data
        # print(f"Datos recibidos por POST: {data}")

        # Puedes procesar los datos, guardarlos en la BD, etc.
        # Por ejemplo, simplemente devolviendo un mensaje de éxito:
        return Response({"message": "Petición POST recibida correctamente en el callback"}, status=status.HTTP_200_OK)
