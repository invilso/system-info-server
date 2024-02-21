import logging
import unittest
from services.router import Router

class TestCommandRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router()
        logging.disable(logging.CRITICAL)

    def test_route_exists(self):
        self.router.route("test_route")(lambda x: x)
        self.assertTrue("test_route" in self.router.routes)

    def test_handle_command_unknown_route(self):
        result = self.router.handle_command("unknown_route", {'127.0.0.1', 44321}, "data")
        self.assertEqual(result, "Error: Unknown route")

if __name__ == '__main__':
    unittest.main()
