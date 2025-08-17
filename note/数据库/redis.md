### redis的使用

1. 打开redis 服务端

2. 打开redis 客户端(Another Redis)

3. 客户端链接reids

4. python代码

    ```python
    import redis
    
    
    # 连接redis数据库
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # 指定密码
    r = redis.Redis(host='localhost', port=6379, db=0, password='your_password')
    
    # 'data' 只能存储redis 允许的数据类型: string,hash,list,set,sorted set
    # json.dumps(data) //data 为列表时
    r.set('name','data')
    ```

    ```python
    # 异步使用redis
    import asyncio
    import redis.asyncio as redis
    
    async def run():
        async with redis.Redis(host='127.0.0.1',port=6379,decode_responses=True) as connect:
            await connect.set('test','我是异步')
            result = await connect.get('test')
            print(result)
    
    asyncio.run(run())
    
    ```

    ```
    # 报错
    class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):
    TypeError: duplicate base class TimeoutError
    
    找到aioredis目录下的exceptions.py文件，定位到14行代码
    class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):
        pass
    
    所以我们修改为如下代码，即可运行
    class TimeoutError(asyncio.exceptions.TimeoutError, RedisError):
        pass
    ```

    