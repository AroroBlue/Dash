import socket
import threading

from decoder import decode_cat048


class UDPReceiver(threading.Thread):

    def __init__(
        self,
        host,
        port,
        source_name,
        aircraft_store
    ):

        super().__init__(daemon=True)

        self.host = host
        self.port = port
        self.source_name = source_name
        self.aircraft_store = aircraft_store

        self.running = True

    def run(self):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        sock.bind((self.host, self.port))

        print(
            f"[{self.source_name}] "
            f"Listening on {self.host}:{self.port}"
        )

        while self.running:

            try:

                data, addr = sock.recvfrom(65535)

                targets = decode_cat048(
                    data,
                    self.source_name
                )

                for target in targets:
                    self.aircraft_store.update_target(target)

            except Exception as e:

                print(
                    f"Receiver error "
                    f"({self.source_name}): {e}"
                )
