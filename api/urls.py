from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(APIView):
    """
    Endpoint para recibir eventos de deliver.ar
    URL: https://tudominio.com/api/callback/
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        Verificación de webhook por parte de deliver.ar
        """
        challenge = request.query_params.get('challenge')
        logger.info(f"🔍 Deliver.ar challenge verification: {challenge}")
        
        # Responder el challenge para confirmar el webhook
        return HttpResponse(challenge or '', content_type='text/plain')

    def post(self, request, *args, **kwargs):
        """
        Recibe eventos cuando algo se publica en deliver.ar
        """
        logger.info("📨 Deliver.ar event received!")
        
        try:
            # Capturar headers importantes
            headers = {
                'content-type': request.META.get('CONTENT_TYPE'),
                'user-agent': request.META.get('HTTP_USER_AGENT'),
                'x-forwarded-for': request.META.get('HTTP_X_FORWARDED_FOR'),
            }
            logger.info(f"📋 Headers: {headers}")
            
            # Obtener datos del evento
            event_data = None
            
            # Intentar obtener datos de diferentes formas
            if request.data:
                event_data = request.data
                logger.info(f"📦 Event data (request.data): {event_data}")
            
            if hasattr(request, 'body') and request.body:
                try:
                    body_data = json.loads(request.body)
                    if not event_data:
                        event_data = body_data
                    logger.info(f"📦 Event data (body): {body_data}")
                except json.JSONDecodeError:
                    logger.info(f"📦 Raw body: {request.body}")

            # 🚀 PROCESAR EL EVENTO AQUÍ
            if event_data:
                self.process_deliver_ar_event(event_data)
            else:
                logger.warning("⚠️ No event data received")
            
            # Respuesta exitosa requerida por deliver.ar
            return HttpResponse(
                "200 OK - Event received successfully",
                content_type='text/plain',
                status=200
            )
            
        except Exception as e:
            logger.error(f"❌ Error processing deliver.ar event: {e}")
            return HttpResponse("Error", status=500)

    def process_deliver_ar_event(self, data):
        """
        🎯 AQUÍ PROCESAS LOS EVENTOS DE DELIVER.AR
        """
        logger.info(f"🔄 Processing deliver.ar event: {data}")
        
        # Ejemplo: detectar tipo de evento
        event_type = data.get('event_type') or data.get('type') or 'unknown'
        
        print(f"\n🎉 ¡NUEVO EVENTO DE DELIVER.AR!")
        print(f"📋 Tipo: {event_type}")
        print(f"📊 Datos completos:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Procesar según el tipo de evento
        if 'order' in str(data).lower():
            print("🛍️ Evento relacionado con pedidos")
            self.handle_order_event(data)
        elif 'delivery' in str(data).lower():
            print("🚚 Evento relacionado con entregas")
            self.handle_delivery_event(data)
        elif 'rider' in str(data).lower() or 'driver' in str(data).lower():
            print("🚴 Evento relacionado con repartidores")
            self.handle_rider_event(data)
        else:
            print("📦 Evento genérico")
            self.handle_generic_event(data)

    def handle_order_event(self, data):
        """Maneja eventos de pedidos"""
        print("💼 Procesando evento de pedido...")
        # Aquí tu lógica para pedidos
        
    def handle_delivery_event(self, data):
        """Maneja eventos de entregas"""
        print("🚛 Procesando evento de entrega...")
        # Aquí tu lógica para entregas
        
    def handle_rider_event(self, data):
        """Maneja eventos de repartidores"""
        print("🏍️ Procesando evento de repartidor...")
        # Aquí tu lógica para repartidores
        
    def handle_generic_event(self, data):
        """Maneja eventos genéricos"""
        print("📋 Procesando evento genérico...")
        # Aquí tu lógica genérica