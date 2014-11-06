# coding=utf8
# from __future__ import division

import redis
import math
from bloomfilter import BloomFilter


class pydrbloomfilter:

    def __init__(
            self, capacity, tolerant,
            redis_conn={}):
        size, hash_count = self._get_cap(capacity, tolerant)
        self.redis_pool = redis.ConnectionPool(
            host=redis_conn.get('host', '127.0.0.1'),
            port=redis_conn.get('port', 6379),
            db=redis_conn.get('db', 0),
        )
        self.bf = BloomFilter(hash_count, size)
        self.bfkey = redis_conn.get('bfkey', 'bf')

    '''
    given M = num_bits, k = num_slices, P = error_rate, n = capacity
    k = log2(1/P)
    solving for m = bits_per_slice
    n ~= M * ((ln(2) ** 2) / abs(ln(P)))
    n ~= (k * m) * ((ln(2) ** 2) / abs(ln(P)))
    m ~= n * abs(ln(P)) / (k * (ln(2) ** 2))

    '''
    def _get_cap(self, capacity, false_prob):
        num_slices = int(math.ceil(math.log(1.0/false_prob, 2)))
        bits_per_slice = int(math.ceil(
            (capacity * abs(math.log(false_prob))) /
            (num_slices * (math.log(2) ** 2))
            ))
        num_bits = num_slices * bits_per_slice
        size = math.ceil(math.log(num_bits, 2))
        return int(size), int(num_slices)

    def add(self, string):
        r_client = redis.Redis(connection_pool=self.redis_pool)
        return r_client.setbit(self.bfkey, self.bf.generate(string), 1)

    def exists(self, string):
        r_client = redis.Redis(connection_pool=self.redis_pool)
        return r_client.getbit(self.bfkey, self.bf.generate(string))

    def __contains__(self, string):
        return self.exists(string)

    def clear(self):
        r_client = redis.Redis(connection_pool=self.redis_pool)
        return r_client.delete(self.bfkey)


if __name__ == '__main__':
    pbl = pydrbloomfilter(300000000, 0.001)
