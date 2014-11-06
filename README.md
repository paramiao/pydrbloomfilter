pydrbloomfilter
===============

pydrbloomfilter is a distributed implement of bloom filter which based on Redis.

It is very simple, I just use the commands that setbit and getbit of Redis to store the
bitarray, and the bloom filter will be persisted in Redis(I just assume your redis server will persisted your data)

usecase:

init bloomfilter

```python
redis_connection = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'bfkey': 'bf'
}
pbl = pydrbloomfilter(10000000, 0.001, redis_connection)
```
add key to bloomfilter
```python
pbl.add('hello world')
```
judge if bloom filter already contains the key
```python
if 'hello world' in pbl:
    print True
```
or
```python
print pbl.exists('hello world')
```
by default, the bloom filter will store in Redis, if you want to clear data, you can delete the bfkey of your redis_connection, or you can do as below:

```python
pbl.clear()
```


thanks to [Creating a Simple Bloom Filter](http://www.maxburstein.com/blog/creating-a-simple-bloom-filter/)
