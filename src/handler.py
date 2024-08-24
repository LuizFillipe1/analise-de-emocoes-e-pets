# Importa as funções dos módulos de rota específicos
from routes.health.health_route import health
from routes.v1.v1_description_route import v1_description
from routes.v2.v2_description_route import v2_description
from routes.v1.v1_analyze_route import v1_analyze
from routes.v2.v2_analyze_route import v2_analyze

# Define o que será exposto quando o módulo for importado
__all__ = [
    'health',
    'v1_description',
    'v2_description',
    'v1_analyze',
    'v2_analyze'
]
