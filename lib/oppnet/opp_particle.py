from lib.oppnet.messagestore import MessageStore
from lib.particle import Particle
from lib.std_lib import black


class Particle(Particle):
    def __init__(self, sim, x, y, color=black, alpha=1, mm_size=0, ms_size=None,
                 ms_strategy=None):
        super().__init__(sim, x, y, color, alpha, mm_size=mm_size)
        if not ms_size:
            ms_size = sim.particle_ms_size
        if not ms_strategy:
            ms_strategy = sim.particle_ms_strategy
        self.send_store = MessageStore(maxlen=ms_size, strategy=ms_strategy)
        self.rcv_store = MessageStore(maxlen=ms_size, strategy=ms_strategy)
        self.signal_velocity = 1
