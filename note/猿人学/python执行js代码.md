### python执行js代码

1. py-mini-racer
2. Pyexecjs
3. subprocess

```python
js_code = """
// console.log(__dirname)
var a = 1;
var f = 1;
function b(){
    return arguments[0] + 100
}
"""
js_code2 = """
(new Promise((f)=>{f()})).then(()=>{
    a = 1000;
    // console.log(a);
    global.result = a;
    }
)
function a(){
    return global.result;
}
"""
```

```python
from py_mini_racer import MiniRacer

ctx = MiniRacer()
ctx.eval(js_code)
result = ctx.call('b', 100)
print(result)
```

```python
import execjs

ctx = execjs.compile(js_code)
result = ctx.call('b', 200)
print(result)
```

```python
import subprocess

result = subprocess.check_output(['node', '-e', js_code.replace('// ', '')])
print(result)
```

```python
import execjs

ctx = execjs.compile(js_code)
result = ctx.call('a')
print(result)
```

```python
import subprocess

result = subprocess.check_output(['node', '-e', js_code.replace('//', '')])
print(result)
```



```python
# 异步并发方案：借助硬盘IO操作

result = subprocess.check_output(['node', '1.js'])
print(result)

import threading

def parallel():
    result = subprocess.check_output(['node', '1.js'])
    print(result)

for i in range(10):
    th = threading.Thread(target=parallel, args=())
    th.start()
```

```python
# 如果要传参怎么办？

with open('1.js') as f:
    js_code = f.read().replace('getTime()', 'getTime() + 900000000000000000')

import threading

def parallel(js_code):
    result = subprocess.check_output(['node', '-e', js_code])
    print(result)

for i in range(10):
    th = threading.Thread(target=parallel, args=(js_code,))
    th.start()
```

```python
# 还有一种情况，就是 js_code 非常大，传进去会报错【比较罕见】
# 那么，我们就只好借助硬盘io了，也可以用内存，先不讲 硬盘便于理解
import time
import threading
import os
import random


def parallel():
    with open('1.js', 'r') as f:
        js_code = f.read().replace('getTime()', 'getTime() + 1900000000000000000')

    file_name = 'result{}.js'.format(time.time() + random.random())
    with open(file_name, 'w') as f:
        f.write(js_code)
    result = subprocess.check_output(['node', file_name])
    print(result)
    os.remove(file_name)  # 删除缓存文件

    
for i in range(10):
    th = threading.Thread(target=parallel, args=())
    th.start()
```

