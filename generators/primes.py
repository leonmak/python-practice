"""
Example of yielding in different areas, which use different contexts.
"""


def get_seive_it(limit):
    """E.g. using sieve"""
    min_size = 2
    r_limit = max(min_size, limit)      # ensure have 0, 1 in list
    r_limit += 1                        # inclusive of limit
    a = [True] * r_limit                # primality listm, still needs memory
    a[0] = a[1] = False                 # 1 and 0 have 1 factor
    for i, is_prime in enumerate(a):    # range [0, number]
        if is_prime:
            yield i                     # state of function is frozen
            for n in range(i**2, limit, i):
                # strike out multiples of itself starting from the square
                # any multiple < its square have already been striked out
                a[n] = False


def get_primes(limit):
    """E.g. using infinite series"""
    num = 0
    while num < limit:
        if is_prime_loop(num):
            yield num
        num += 1


def is_prime_loop(n):
    if n < 2:
        return False
    else:
        for i in range(2, n):
            if n % i == 0:
                return False
        return True


def is_number_prime(itr, number):
    """Exhaust iterator until verify prime"""
    print("Primes: ", end='')
    is_prime = False
    for prime in itr:
        print(f"{prime} ", end='')
        if prime == number:
            is_prime = True
            break
        elif prime > number:
            is_prime = False
            break
    return number, is_prime


if __name__ == '__main__':
    # Get Primes example

    r_bound = 30000
    n = 21061   # import random; random.randint(20000, r_bound)

    # E.g. Using sieve of eratosthenes
    # Use big number like 100k, each call is faster,
    # but cannot use infinity as uses more memory cos of Boolean list
    num, was_prime = is_number_prime(get_seive_it(r_bound), n)
    print(f"\n{num} {'is' if was_prime else 'is not'} a prime")

    # E.g. Using generator for yielding each number
    # Can use infinity, but each call is slow cos of for-loop checking.
    # but can use sys.maxsize (pseudo-infinity) as no list.
    num, was_prime = is_number_prime(get_primes(r_bound), n)
    print(f"\n{num} {'is' if was_prime else 'is not'} a prime")
