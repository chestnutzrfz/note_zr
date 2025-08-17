### 无限debugger

##### 实现无限debugger的方法

1.debugger关键词（最经典的了，基础课大家应该太熟悉了，我们经常用这个关键词做调试）    

2. eval('debugger') 原理跟1类似，只不过是在虚拟机里面执行debugger的方法    
3. Function('debugger')() 及其变种 原理跟2类似，只不过是在虚拟机里面执行匿名函数，匿名函数里有debugger的方法 



##### 解决无限debugger

1. 优先尝试 Never pause here （最方便快捷，但是最卡，也最容出问题）       

2. 次优先尝试重写调用函数            

    如： Function = function(){}              

    setInterval = function(){}            

    缺陷：容易破坏业务逻辑，导致控制流变化        

3. 使用 AutoResponse/mapping/overrides 替换            

    缺陷：操作稍微有一点点的麻烦，对动态情况的支持不太好，也可能会改变控制流走向



