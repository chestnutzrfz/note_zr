### hook

```js
_a = a   // 这一步叫保留原始函数
a = function(){   // 这一步叫重写函数
 	console.log(arguments[1])   //  实现我们想要功能和逻辑的地方
    return _a(arguments)        //  保留原始的功能，让原来的内容可以正常执行
}
```



```js
_a = a
a = function(){
 	console.log(arguments[1])
    return _a.apply(this,arguments)
}
```

##### 无限debugger

```js
var _constructor = constructor;
Function.prototype.constructor = function(s) {
    if (s == "debugger") {
        console.log(s);
        return null;
    }
    return _constructor(s);
}

//去除无限debugger
Function.prototype.__constructor_back = Function.prototype.constructor ;
Function.prototype.constructor = function() {
    if(arguments && typeof arguments[0]==='string'){
        //alert("new function: "+ arguments[0]);
        if( "debugger" === arguments[0]){
            // arguments[0]="consoLe.Log(\"anti debugger\");";
            //arguments[0]=";";
            return
    }
    }
    return Function.prototype.__constructor_back.apply(this,arguments);
};

var _Function = Function;
Function = function(s) {
    if (s == "debugger") {
        console.log(s);
        return null;
    }
    return _Function(s);
}

```

##### cookie生成hook

```js
(function () {
    var cookieTemp = "";
    Object.defineProperty(document, 'cookie', {
        set: function (val) {
            if (val.indexOf('FSSBBIl1UgzbN7N80T') != -1) {
                debugger;
            }
            cookieTemp = val;
            return val;
        },
        get: function () {
            return cookieTemp;
        }
    });
})();
//方式二  油猴
https://github.com/CC11001100/js-cookie-monitor-debugger-hook
```

##### js自动吐环境

```js
// 代理器封装
function get_enviroment(proxy_array) {
    for(var i=0; i<proxy_array.length; i++){
        handler = '{\n' +
            '    get: function(target, property, receiver) {\n' +
            '        console.log("方法:", "get  ", "对象:", ' +
            '"' + proxy_array[i] + '" ,' +
            '"  属性:", property, ' +
            '"  属性类型:", ' + 'typeof property, ' +
            // '"  属性值:", ' + 'target[property], ' +
            '"  属性值类型:", typeof target[property]);\n' +
            '        return target[property];\n' +
            '    },\n' +
            '    set: function(target, property, value, receiver) {\n' +
            '        console.log("方法:", "set  ", "对象:", ' +
            '"' + proxy_array[i] + '" ,' +
            '"  属性:", property, ' +
            '"  属性类型:", ' + 'typeof property, ' +
            // '"  属性值:", ' + 'target[property], ' +
            '"  属性值类型:", typeof target[property]);\n' +
            '        return Reflect.set(...arguments);\n' +
            '    }\n' +
            '}'
        eval('try{\n' + proxy_array[i] + ';\n'
        + proxy_array[i] + '=new Proxy(' + proxy_array[i] + ', ' + handler + ')}catch (e) {\n' + proxy_array[i] + '={};\n'
        + proxy_array[i] + '=new Proxy(' + proxy_array[i] + ', ' + handler + ')}')
    }
}
proxy_array = ['window', 'document', 'location', 'navigator', 'history','screen']
get_enviroment(proxy_array)

```



##### eval的hook

```js
_eval = eval;
eval= function(){
	if (arguments[0].indexOf('debugger') === -1)
    return _eval(arguments[0])
}
```

eval一般只有一个参数, eval执行在单独一个虚拟机里不需要指定this

##### hook随机数

```js
Date.now = function now() {
    return 1661986251253
};
Date.parse = function () {
    return 1661986251253
};
Date.prototype.valueOf = function () {
    return 1661986251253
};
Date.prototype.getTime = function () {
    return 1661986251253
};
Date.prototype.toString = function () {
    return 1661986251253
};
Performance.prototype.now = function now() {
    return Number('1661986251253'.slice(8))
}
Math.random = function random() {
    return 0.08636862211354912
};
window.crypto.getRandomValues = function getRandomValues(array32, ...args) {
    return array32;
}

```



##### 重点

怎么找到需要hook的函数在哪里

