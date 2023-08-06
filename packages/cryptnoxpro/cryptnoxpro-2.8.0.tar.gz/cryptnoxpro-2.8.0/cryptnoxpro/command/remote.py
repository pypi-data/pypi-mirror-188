import cryptnoxpy

from .command import Command
from .remote import client

try:
    import enums
except ImportError:
    from .. import enums


class Remote(Command):
    _name = enums.Command.REMOTE.value

    def _execute(self, card: cryptnoxpy) -> int:
        actions = {
            "client": Remote._client,
            "server": Remote._server,
            "txmanager": Remote._txmanager,
        }

        try:
            result = actions[self.data.action](card)
        except KeyError:
            print("Method not supported with this card type.")
            result = 1

        return result

    def _client(self, card: cryptnoxpy.Card) -> int:
        client.start(card)

    def _server(self):
        return 0

    def _txmanager(self):
        return 0
