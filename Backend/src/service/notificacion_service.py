from ..repository import NotificacionRepository
from ..util.web_util import add_wrapper
import json

class NotificacionService:

    def get_notificacion(self, notificacion_repository: NotificacionRepository):
        notificacion = []
        data = notificacion_repository.get_notificacion_bd()
        for result in data:
            notificacion.append(
                {
                    'idnotificacion': result[0],
                    'idproceso': result[1],
                    'radicado': result[2],
                    'fechaAutorizacion': str(result[3]),
                    'email': result[4]
                }
            )
        return notificacion

    def get_notificacion_proceso(self, notificacion_repository: NotificacionRepository, idproceso):
        notificacion = []
        model = {}
        emails = ''
        data = notificacion_repository.get_notificacion_proceso_bd(idproceso)
        for result in data:
            model = {
                'idnotificacion': result[0],
                'idproceso': result[1],
                'radicado': result[2],
                'fechaAutorizacion': str(result[3]),
                'correos': result[4]
            }
            emails = json.loads(result[4])

            for email in emails:
                # print('------- EMAIL ---- ', email['value'])
                model[email['prop']] = email['value']

            notificacion.append(model)
        return notificacion

    def notificacion_insert(self, notificacion_repository: NotificacionRepository, notificacion):
        notificacion_repository.notificacion_insert_bd(notificacion)
        return add_wrapper(['notificacion registrada con éxito!'])

    def notificacion_update(self, notificacion_repository: NotificacionRepository, datanotificacion):
        notificacion_repository.notificacion_update_bd(datanotificacion)
        return add_wrapper(['notificacion actualizada con éxito!'])

    def notificacion_delete(self, notificacion_repository: NotificacionRepository, idtercero):
        notificacion_repository.notificacion_delete_bd(idtercero)
        return add_wrapper(['notificacion borrada con éxito!'])