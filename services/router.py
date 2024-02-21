import json
import sys
from services.main import init_logger, is_jsonable

logger = init_logger(__name__)

class Router:
    def __init__(self):
        self.routes = {}

    def route(self, route):
        def decorator(func):
            self.routes[route] = func
            return func
        return decorator

    def handle_command(self, route, *args, **kwargs):
        handler = self.routes.get(route)
        if handler:
            result = handler(*args, **kwargs)
            if isinstance(result, str):
                logger.debug('The data was transmitted "as is"')
                return result
            if is_jsonable(result):
                logger.debug('The data has been serialized into json')
                return json.dumps(result, separators=(',', ':'))
            else:
                logger.error('Return object is not jsonable')
                return 'Error: Return object is not jsonable'
        else:
            logger.error('Unknown route')
            return "Error: Unknown route"
        
        
class ConsoleRouter(Router):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_console_commands(self):
        if len(sys.argv) < 2:
            return "Usage: python manage.py [route] [parameters]"
        
        route = sys.argv[1]
        if not self.routes.get(route):
            return f"Error: Unknown route '{route}'"
        
        data = sys.argv[2:]
        if len(data) > 0:
            return self.handle_command(route, data)
        else:
            return self.handle_command(route)
