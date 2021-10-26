from ..repository import EmpresaRepository

class EmpresaService:

    def get_empresas(self, empresa_repository: EmpresaRepository, servicio):
        empresas = []
        data = empresa_repository.get_empresas_servicio_bd(servicio)
        for result in data:
            empresas.append(
                {
                    'id_empresa': result[0],
                    'nombre': result[1],
                    'sigla': result[2],
                    'nit': result[3],
                    'cod_servicio': result[4],
                    'servicio': result[5],
                }
            )
        return empresas