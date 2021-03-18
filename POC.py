import types
import multiprocessing as mp
import threading
import time


class output:
    def __init__(self, queue=None):
        self.queue = queue
        threading.Thread(target=self.run).start()

    def run(self):
        while True:
            now = time.time()
            self.queue.put(now)
            time.sleep(1)


def importCode(code, name):
    """ code can be any object containing code -- string, file object, or
       compiled code object. Returns a new module object initialized
       by dynamically importing the given code and optionally adds it
       to sys.modules under the given name.
    """
    module = types.ModuleType(name)
    exec(code, module.__dict__)
    return module


class Bootstrap:
    def __init__(self, code, queue=None):
        self.code = code
        self.queue = queue
        self.run()

    def run(self):
        module = importCode(self.code, 'Webshop')
        module.Webshop(23, queue=self.queue)


if __name__ == '__main__':
    code = """
class Webshop:
    def __init__(self, a, queue=None):
        self.a = a
        self.queue = queue
        self.run()

    def run(self):
        while True:
            if not self.queue.empty():
                print(self.queue.get())
"""
    queue = mp.Queue()
    output(queue=queue)

    # bootstrap = Bootstrap(code, queue=queue)

    process = mp.Process(target=Bootstrap,
                         name='TEST',
                         args=(code,),
                         kwargs=({'queue': queue}))
    process.start()
