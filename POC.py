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
        by dynamically importing the given code.
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
        module = importCode(self.code, 'POC')
        module.POC('Hello World', queue=self.queue)


if __name__ == '__main__':
    code = """
class POC:
    def __init__(self, message, queue=None):
        self.message = message
        self.queue = queue
        self.run()

    def run(self):
        while True:
            if not self.queue.empty():
                print('{message} the time is {time} seconds past 1970'.format(message=self.message, time=self.queue.get()))
"""
    queue = mp.Queue()
    output(queue=queue)
    
    process = mp.Process(target=Bootstrap,
                         name='TEST',
                         args=(code,),
                         kwargs=({'queue': queue}))
    process.start()
