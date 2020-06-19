class AbstractList:
	"""Abstract base class implementing common methods.
	"""
	def isEmpty(self):
		return False
	def __add__(self, other):
		"""Overloads the + operator to act as concat"""
		return self.concat(other)
    def __str__(self):
        """Returns a conventional representation of the list as a string"""
        return '[' + self.commaElements(7) + ']'
    def takeWhile(self, predicate):
        """returns a list containing the elements of self as far as
        (but excluding) the first element for which predicate is
        false;  predicate is a function on the elements of self
        that returns a Boolean.
        """
        if predicate(self.head()) == True:
            return ConsList(self.head(), self.tail().takeWhile(predicate))
        else:
            return EmptyList()
    def do(self, function):
        """Applies function to every element of this list. Returns no result."""
        function(self.head())
        self.tail().do(function)
    def detect(self, predicate):
        """Returns the first element of this list for which
        predicate is true.  If there is no such element,
        raises the exception IndexError("No such object")
        """
        if predicate(self.head()) == True:
            return self.head()
        else:
            return self.tail().detect(predicate)

class EmptyList(AbstractList):
    """ Represents an empty list. 
    
    >>> set(dir(EmptyList)).issuperset(listInterface)
    True
    >>> EmptyList().length()
    0
    >>> a = EmptyList()
    >>> a.next()
    Traceback (most recent call last):
      File "/usr/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
      File "<doctest lists.EmptyList[3]>", line 1, in <module>
        a.next()
      File "listObjects4.py", line 40, in next
        raise ValueError("Can't return next element of the empty list")
    ValueError: Can't return next element of the empty list
    """
    def isEmpty(self):
        return True
    def head(self):
        raise ValueError("Can't take `head` of the empty list")
    def tail(self):
        raise ValueError("Can't take `tail` of the empty list")
    def __repr__(self):
        return 'EmptyList()'
    def length(self):
        """ There are no elements in an empty list."""
        return 0
    def next(self):
        """ Returns the next element of the list."""
        raise ValueError("Can't return next element of the empty list")
    def concat(self, other):
        """Returns a concatenated list of the form self, followed by other"""
        return other
    def commaElements(self, count):
        """Since we are an empty list, there are no comma separated values in the list"""
        return ""
    def takeWhile(self, predicate):
        """returns a list containing the elements of self as far as
        (but excluding) the first element for which predicate is
        false;  predicate is a function on the elements of self
        that returns a Boolean.
        """
        return EmptyList()
    def dropWhile(self, predicate):
        """returns a list like self except that all of the leading
        elements for which predicate is true have been removed.
        Thus, predicate will be false on the first element of the
        result; predicate is a function on the elements of self
        that returns a Boolean.
        """
        return EmptyList()  
    def do(self, function):
        """Applies function to every element of this list
        We're an empty list. We don't have anything to "do" something on.
        Returns no result.
        """
        return
    def detect(self, predicate):
        """Returns the first element of this list for which
        predicate is true.  If there is no such element,
        raises the exception IndexError("No such object")
        """
        raise IndexError("No such object")
      
class ConsList(AbstractList):
    """ Represents a non-empty list.
    
    >>> set(dir(ConsList)).issuperset(listInterface)
    True
    >>> alist = ConsList(1, ConsList(2, ConsList(3, EmptyList())))
    >>> blist = ConsList(4, ConsList(5, ConsList(6, ConsList(7, EmptyList()))))
    >>> str(alist)
    '[1, 2, 3]'
    >>> alist.next()
    2
    >>> alist.length()
    3
    >>> alist.concat(blist)
    ConsList(1, ConsList(2, ConsList(3, ConsList(4, ConsList(5, ConsList(6, ConsList(7, EmptyList())))))))
    >>> blist.concat(alist)
    ConsList(4, ConsList(5, ConsList(6, ConsList(7, ConsList(1, ConsList(2, ConsList(3, EmptyList())))))))
    >>> alist + blist
    ConsList(1, ConsList(2, ConsList(3, ConsList(4, ConsList(5, ConsList(6, ConsList(7, EmptyList())))))))
    >>> (alist + blist).length() - (blist + alist).length()
    0
    >>> clist = alist + blist + ConsList(8, ConsList(9, ConsList(10, EmptyList())))
    >>> str(clist)
    '[1, 2, 3, 4, 5, 6, 7, 8...]'
    >>> oneToFifty = nums(1, 51)
    >>> oneToTwenty = oneToFifty.takeWhile(lambda x: x <= 20)
    >>> oneToTwenty.length()
    20
    >>> oneToTwenty.head()
    1
    >>> oneToTwenty.tail().tail().head()
    3
    >>> twentyOneOn = oneToFifty.dropWhile(lambda x: x <= 20)
    >>> twentyOneOn.length()
    30
    >>> twentyOneOn.head()
    21
    >>> twentyOneOn.tail().tail().head()
    23
    >>> alist.do(lambda each: print(each))
    1
    2
    3
    >>> clist.detect(lambda each: each > 7)
    8
    """
    def __init__(self, head, tail):
        self.__head = head
        self.__tail = tail
    def head(self):
        return self.__head
    def tail(self):
        return self.__tail
    def __repr__(self):
        return "ConsList(" + self.head().__repr__() + ", " + self.tail().__repr__() + ")"
    def length(self):
        """ This list is one element longer than its tail."""
        return 1 + self.tail().length()
    def next(self):
        """ Returns the next element of the list."""
        return self.tail().head()
    def concat(self, other):
        """Returns a concatenated list of the form self, followed by other"""
        return ConsList(self.head(), self.tail().concat(other))
    def commaElements(self, count):
        """Helper method that returns a comma separated string of list elements"""
        if self.tail().isEmpty() == True or count == 0:
            listRep = self.head().__repr__()
        else:
            listRep = self.head().__repr__() + ", " + self.tail().commaElements(count - 1)
        if count == 0:
            listRep = listRep + "..."
        return listRep
    def dropWhile(self, predicate):
        """returns a list like self except that all of the leading
        elements for which predicate is true have been removed.
        Thus, predicate will be false on the first element of the
        result; predicate is a function on the elements of self
        that returns a Boolean.
        """
        if predicate(self.head()) == True:
            return self.tail().dropWhile(predicate)
        else:
            return ConsList(self.head(), self.tail())

class InfiniteList(AbstractList):
    '''Represents an infinite list, defined by an initial value, and a
    function that generates the next value.  So, for example, the Natural
    numbers would be represented by the initial value 0, and the function
    λn. n + 1.
    >>> set(dir(InfiniteList)).issuperset(listInterface)
    True
       
    Examples:
    >>> nats = InfiniteList(0, lambda n: n + 1)
    >>> nats.length()
    inf
    >>> nats.head()
    0
    >>> nats.tail().head()
    1
    >>> nats.tail().tail().head()
    2
    >>> nats.tail().tail().tail().head()
    3
    >>> str(nats)
    '[0, 1, 2, 3, 4, 5, 6, 7...]'
    >>> str(nats) == repr(nats)
    True
    >>> alist = InfiniteList(0, lambda n: n + 1)
    >>> blist = alist.takeWhile(lambda x: x <= 5)
    >>> str(blist)
    '[0, 1, 2, 3, 4, 5]'
    >>> nats.do(lambda each: print(each))
    Traceback (most recent call last):
      File "/usr/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
      File "<doctest lists.InfiniteList[12]>", line 1, in <module>
        nats.do(lambda each: print(each))
      File "test.py", line 23, in do
        self.tail().do(function)
      File "test.py", line 23, in do
        self.tail().do(function)
      File "test.py", line 23, in do
        self.tail().do(function)
      [Previous line repeated 988 more times]
      File "test.py", line 237, in tail
        return InfiniteList(self.next(), self.__nextFun)
    RecursionError: maximum recursion depth exceeded
    >>> nats.detect(lambda each: each > 20) 
    21
    '''
    def __init__(self, initial, nextFun):
        self.__initial = initial
        self.__nextFun = nextFun
    def head(self):
        return self.__initial
    def tail(self):
        return InfiniteList(self.next(), self.__nextFun)
    def next(self):
        return self.__nextFun(self.__initial)
    def length(self):
        return float('inf')
    def __repr__(self):
        """Returns a string representation of the infinite list"""
        return self.__str__()
    def commaElements(self, count):
        element = self.__initial
        listRep = ""
        for i in range(count):
            listRep = listRep + str(element) + ", "
            element = self.__nextFun(element)
        listRep = listRep + str(element)
        return listRep + "..."
    def dropWhile(self, predicate):
        """returns a list like self except that all of the leading
        elements for which predicate is true have been removed.
        Thus, predicate will be false on the first element of the
        result; predicate is a function on the elements of self
        that returns a Boolean.
        >>> alist = InfiniteList(0, lambda n: n + 1)
        >>> blist = alist.dropWhile(lambda x: x <= 5)
        >>> str(blist)
        '[6, 7, 8, 9, 10, 11, 12, 13...]'
        """
        if predicate(self.head()) == True:
            return self.tail().dropWhile(predicate)
        else:
            return InfiniteList(self.head(), self.__nextFun)
    def concat(self, other):
        """Returns the other InfiniteList concatenated to self.
        Probably won't print the second half though.
        
        >>> nats = InfiniteList(0, lambda n: n + 1)
        >>> wholes = InfiniteList(1, lambda n: n + 1)
        >>> str(nats.concat(wholes))
        '[0, 1, 2, 3, 4, 5, 6, 7...]'
        >>> str(nats + wholes)
        '[0, 1, 2, 3, 4, 5, 6, 7...]'
        """
        return InfiniteList(self.__initial, self.__nextFun)
        
listInterface = {'head', 'tail', 'next', 'isEmpty', 'takeWhile',\
                 'dropWhile', 'length', 'do', 'detect', 'concat',\
                 '__add__', 'commaElements'}  
  
def classImplements(c, ms):
    """c is a class, and ms is a set of method names.  
    Returns True if c implements all the methods in c.  
    Complains otherwise, and returns False
    """
    result = True
    for n in ms:
        m = getattr(c, n, False)
        if not (m and callable(m)):
            print(c, "does not have method", n)
            result = False
    return result
        
def nums(lo, hi):
    """ Returns a list containing the numbers from lo up to but excluding hi
    
    >>> str(nums(0, 5))
    '[0, 1, 2, 3, 4]'
    >>> str(nums(3,2))
    '[]'
    """
    return ConsList(lo, nums(lo+1, hi)) if lo < hi else EmptyList()
  
def powers2(n):
    """ Returns a list containing the first n powers of 2
    
    >>> powers2(6)
    '[1, 2, 4, 8, 16, 32]'
    """
    exponents = EmptyList()
    for exponent in reversed(range(n)):
        exponents = ConsList(pow(2, exponent), exponents)
    return str(exponents)
    
# Standard boilerplate to call the testmod() function.
if __name__ == '__main__':
    from doctest import testmod
    testmod(name='lists', verbose=True, raise_on_error=False)
