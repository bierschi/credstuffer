import os
import logging
from tempfile import mkdtemp
from shutil import rmtree
from stem.process import launch_tor_with_config
from stem.control import Controller
from stem.util import term
from stem import Signal


class Tor:
    """ class Tor to make requests over the tor network

    USAGE:
            tor = Tor()
            tor.launch()
            session_tor = requests.Session()
            session_tor.proxies['http'] = 'socks5h://localhost:9050'
            session_tor.proxies['https'] = 'socks5h://localhost:9050'
            cur_ip = session_tor.get(url='http://httpbin.org/ip')
            tor.trigger_new_ip()

    """
    def __init__(self, socks_port=9050, control_port=9051):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class Tor')

        self.socks_port   = socks_port
        self.control_port = control_port

        self.data_directory = mkdtemp()

        self.default_config = {
            "SOCKSPort": str(self.socks_port),
            "ControlPort": str(self.control_port),
            "DataDirectory": self.data_directory,
            "ExitRelay": str(0),
        }
        self.process = None
        self.controller = None

    def __del__(self):
        """ destructor

        """
        self.quit()

    def launch(self):
        """ launches a new tor process

        :return: created process
        """

        self.process = launch_tor_with_config(config=self.default_config, init_msg_handler=self._bootstrap_lines, take_ownership=True)

        self.controller = Controller.from_port(port=self.control_port)
        self.controller.authenticate()

        return self.process

    def quit(self):
        """kills the current tor process and removes the data directory

        """

        # kill process
        self.process.kill()

        # remove tmp folder
        if os.path.exists(self.data_directory):
            rmtree(self.data_directory)

    def trigger_new_ip(self):
        """ triggers an ip change to the Tor circuit

        """

        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def _bootstrap_lines(self, line):
        """ bootstraps logger lines

        """
        if "Bootstrapped" in line:
            self.logger.info("Tor logger outputs: {}".format(line))
            print(term.format(line, term.Color.BLUE))

        if "100%" in line:
            self.logger.info("[%05d] Tor process executed successfully" % self.socks_port)
            print("[%05d] Tor process executed successfully" % self.socks_port)



