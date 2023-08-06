"""
    Ku
    ==
    single-thread async tcp proxy
"""

from threading import Thread
from select import select
from socket import socket
from typing import Union

class Reject(object):
    pass

class Pass(object):
    pass

class tcpsession(object):

    def __init__(self, client: socket, server: socket, proxy):
        pass

    def clientbound(self, data: bytes) -> Union[bytes, Reject, Pass]:
        pass

    def serverbound(self, data) -> Union[bytes, Reject, Pass]:
        pass

    def connection_made(self) -> None:
        pass

    def connection_lost(self, side: Union[socket, None], err: Union[Exception, None]) -> None:
        pass

class ku(object):

    fd: list  # tracked file descriptors
    ss: list  # [[<socket Client>, <socket Upstream>, <tcpsession Session>], ...]

    socket: socket  # listening socket
    thread: Thread  # polling thread
    upstream: tuple  # upstream proto, host, port

    alive: bool = True  # alive marker

    @staticmethod
    def htphp(host: tuple):
        """
            convert host tuple to proto, host, port
        """
        x = host[0].split(']')
        if len(x) == 2:
            return 23, x[0][1:], host[1]
        return 2, host[0], host[1]

    def __init__(self, listen: tuple, upstream: tuple, session: tcpsession = tcpsession, maxcon: int = -1):

        self.fd: list = []
        self.ss: list = []

        self.upstream = self.htphp(upstream)
        self.session = session
        self.maxcon = maxcon

        proto, host, port = self.htphp(listen)
        self.socket = socket(proto, 1)
        self.socket.bind((host, port))
        self.socket.listen()
        self.fd.append(self.socket)

        self.thread = Thread(target=self.poll)
        self.thread.start()

    def shutdown(self):
        self.alive = False

    def terminate(self, session: tcpsession):
        for s in self.ss.copy():
            if s[2] == session:
                session.connection_lost(None, RuntimeError("Internal terminate request"))
                self.ss.remove(s)
                self.fd.remove(s[0])
                self.fd.remove(s[1])
                s[1].close()
                s[0].close()

    def _handle_socket_disconnect(self, fd, err):        
        for s in self.ss.copy():
            if s[0] == fd or s[1] == fd:
                # found session
                s[2].connection_lost(fd, err)
                self.ss.remove(s)
                self.fd.remove(s[0])
                self.fd.remove(s[1])
                s[1].close()
                s[0].close()

    def poll(self):
        while self.alive:
            # select()
            fds = select(self.fd, [], [], 0)[0]

            if self.socket in fds:
                # check limitations
                if len(self.ss) != self.maxcon:
                    # new client
                    c, addr = self.socket.accept()

                    # new upstream
                    u = socket(self.upstream[0], 1)
                    try:
                        u.connect(self.upstream[1:])
                    except Exception as e:
                        print(F"Failed to connect to the server due to an error: {e}")
                        c.close()
                        continue

                    # create new instance of tcpsession class
                    s = self.session(c, u, self)
                    s.connection_made()

                    self.ss.append([c, u, s])
                    self.fd.append(c)
                    self.fd.append(u)
                fds.remove(self.socket)
            print(fds) if self.socket in fds else None
            for f in fds:
                try:
                    data = f.recv(65535)
                except Exception as e:
                    self._handle_socket_disconnect(f, e)
                    continue

                if len(data) < 1:
                    self._handle_socket_disconnect(f, None)
                    continue

                for s in self.ss:
                    if f == s[0]:
                        hr = s[2].serverbound(data)
                        if isinstance(hr, bytes):
                            data = hr
                        elif hr is Reject:
                            continue
                        elif hr is not Pass and hr is not None:
                            raise RuntimeError(F"Handler returned undefined type! {hr.__class__}")
                        try:
                            s[1].sendall(data)
                        except Exception as e:
                            self._handle_socket_disconnect(f, e)

                    elif f == s[1]:
                        hr = s[2].clientbound(data)
                        if isinstance(hr, bytes):
                            data = hr
                        elif hr is Reject:
                            continue
                        elif hr is not Pass and hr is not None:
                            raise RuntimeError(F"Handler returned undefined type! {hr.__class__}")
                        try:
                            s[0].sendall(data)
                        except Exception as e:
                            self._handle_socket_disconnect(f, e)
