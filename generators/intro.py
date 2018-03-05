"""
Generators are: iterators returned / yielded by (generator) functions
Mostly generators refer to the iterator returned
Pauses and captures state / context of execution and allows 'lazy evaluation'

Iterators are: objects that have an __iter__ and a __next__
`next(itr)` to call __next__, `iter(itr)`

Why `yield` instead of `return`?
- Give future value using saved state instead of returning control of execution

Prime numbers are: numbers that have 2 factors: 1 and itself

Links:
https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/
https://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators
"""
import collections
import types


def print_descriptions():
    print("Generator is subclass of Iterator? "
          f"{issubclass(types.GeneratorType, collections.Iterator)}")
    print("Iterator is subclass of Iterable? "
          f"{issubclass(collections.Iterator, collections.Iterable)}\n")


def gen_expressions():
    def yes(stop):
        for _ in range(stop):
            yield 'yes'
    stop = 10
    yes_genr_fn_it = yes(stop)
    yes_genr_expn_it = ('yes' for _ in range(stop))
    for s_fn_el, s_gnr_el in zip(yes_genr_fn_it, yes_genr_expn_it):
        # zip also returns an iterator
        if s_fn_el != s_gnr_el:
            raise ValueError('not equal strings')
    print(f"Type of called yield-fn `yes(stop)`: {type(yes_genr_fn_it)}, \n"
          f"Type of generator expn: {type(yes_genr_expn_it)}\n")


if __name__ == '__main__':
    print_descriptions()
    gen_expressions()

