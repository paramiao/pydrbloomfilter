# coding=utf8
from __future__ import absolute_import

import mmh3


class BloomFilter:

    def __init__(self, hash_count, size):
        self.hash_count = hash_count
        self.size = size

    def generate(self, string):
        bit_array = ['0' for s in xrange(self.size)]
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            bit_array[result] = '1'
        return int(''.join(bit_array), 2)


if __name__ == '__main__':
    bf = BloomFilter(10, 32)
    print bf.generate('hahdfl')
