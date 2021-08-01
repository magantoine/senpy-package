class IterableDecorator:
    """
    Decorates an Iterable. A class is iterable if it defines
    a method __iter__.
    """
    def __init__(self, iterable):
        self.iterable = iterable
        self.n = 0

    def __iter__(self):
        #local var are faster than calling self. each time
        iterable = self.iterable 
        n = self.n
        for obj in iterable:
            yield obj
            print(n)
            n += 1
        print(f'Finished {n} iterations')

def main():
    for i in IterableDecorator(range(10)):
        pass

if __name__ == '__main__':
    main()