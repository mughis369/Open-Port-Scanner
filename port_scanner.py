import socket, threading
from traceback import print_exc
import os, sys, time


class AllThreadsStarted(Exception):
    pass


class IPv4PortScanner(object):
    def __init__(self, domain, timeout=2.0, port_range=(1024, 65535), threadcount=10):
        self.domain = domain
        self.timeout = timeout
        self.port_range = port_range
        self.threadcount = threadcount
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._ports_active = []
        self._ports_being_checked = []

        self._next_port = self.port_range[0]

    def check_port_(self, port):
        "If connects then port is active"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(self.timeout)
        try:
            sock.connect((self.domain, port))
            with self._lock:
                self._ports_active.append(port)
            print("Found active port {}".format(port))
            sock.close()
        except socket.timeout:
            return
        except:
            pass
            # pdb.set_trace()

    def check_port(self, port):
        "updates self._ports_being_checked list on exit of this method"
        try:
            self.check_port_(port)
        finally:
            self._condition.acquire()
            self._ports_being_checked.remove(port)
            self._condition.notifyAll()
            self._condition.release()

    def start_another_thread(self):
        if self._next_port > self.port_range[1]:
            raise AllThreadsStarted()
        port = self._next_port
        self._next_port += 1
        t = threading.Thread(target=self.check_port, args=(port,))
        # update books
        with self._lock:
            self._ports_being_checked.append(port)
        t.start()

    def run(self):
        try:
            while True:
                self._condition.acquire()
                while len(self._ports_being_checked) >= self.threadcount:
                    # we wait for some threads to complete the task
                    self._condition.wait()
                slots_available = self.threadcount - len(self._ports_being_checked)
                self._condition.release()
                for i in range(slots_available):
                    self.start_another_thread()
        except AllThreadsStarted:
            print("All threads started ...")
        except:
            pass


if __name__ == "__main__":
    import sys

    domain = sys.argv[1]
    
    if domain is not None:
        try:
            port_s = int(sys.argv[2])
            port_e = int(sys.argv[3])
        except:
            port_s = 1
            port_e = 65535
            print(f"Setting default port range: {port_s} - {port_e}")
        print("Scaning " + domain)
        scanner = IPv4PortScanner(domain=domain, port_range=(port_s, port_e))
        scanner.run()
        print(f"ports scanned: " {str(port_s)} "-" {str(port_e)})
        print("open found: " {str(scanner._ports_active)})
    else:
        print("ERR: domain name is required!")

