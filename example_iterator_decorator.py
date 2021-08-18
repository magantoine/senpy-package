from time import sleep 
from datetime import datetime
from senpy import ntm

class IterableDecorator:
    """
    Decorates an Iterable. A class is iterable if it defines
    a method __iter__.
    """
    def __init__(self, iterable):
        self.iterable = iterable
        self.currentIteration = 0
        self.totalIteration = len(iterable)
        self.timeStarted = datetime.utcnow()


    def __iter__(self):
        #local var are faster than calling self. each time
        iterable = self.iterable 
        currentIteration = self.currentIteration

        for obj in iterable:
            yield obj
            print(currentIteration)
            currentIteration += 1
            # sleep(2)

        print(f'Finished {n} iterations')

def main():
    for i in ntm(range(10), name='test'):
        pass

if __name__ == '__main__':
    main()
