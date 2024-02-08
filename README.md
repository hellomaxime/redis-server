# redis-server

Redis is an in-memory key-value NoSQL database.

This is a coding challenge from https://codingchallenges.fyi/challenges/challenge-redis/.  
It aims to build a lite version of Redis with all the functionality of the first version of Redis.

The server was built using Python (but prefer C, Rust or Golang for performance) and test-driven development approach.

### 1 - protocol  
- RESP is the protocol used to communicate with a Redis server
- Clients send commands to a Redis Server as a RESP Array of Bulk Strings
- Server replies with one of the RESP type
- Need to implement a functionality to serialize and deserialize messages

### 2 - server  
- Create a server that listens on port `6379`
- Sockets, Threads, Concurrency
- Use redis-cli to communicate with redis server

### 3 - commands
- PING
- ECHO
- SET (with expiration options)
- GET
- EXISTS
- DEL
- INCR
- DECR
- LPUSH
- RPUSH
- SAVE

### 4 - performance check
- You can use redis-benchmark to check concurrency and performance
- The redis-benchmark utility simulates running commands done by N clients while at the same time sending M total queries.
