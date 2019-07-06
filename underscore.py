class Underscore:
    def map(self, iterable, callback):
        for x in range(len(iterable)):
            iterable[x] = callback(iterable[x])
        return iterable
    
    def find(self, iterable, callback):
        for val in iterable:
            if callback(val):
                return val
    
    def filter(self, iterable, callback):
        new_arr = []
        for val in iterable:
            if callback(val):
                new_arr.append(val)
        return new_arr
    
    def reject(self, iterable, callback):
        new_arr = []
        for val in iterable:
            if not callback(val):
                new_arr.append(val)
        return new_arr

_ = Underscore()
_.map([1,2,3], lambda x: x*2) # should return [2,4,6]
found = _.find([1,2,3,4,5,6], lambda x: x > 4) # should return the first value that is greater than 4
_.filter([1,2,3,4,5,6], lambda x: x%2==0) # should return [2,4,6]
reject = _.reject([1,2,3,4,5,6], lambda x: x%2==0) # should return [1,3,5]
