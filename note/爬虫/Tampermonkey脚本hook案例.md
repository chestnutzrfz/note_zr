# JS注入：油猴Tampermonkey脚本hook教程





### @介绍

```stylus
油猴：Tampermonkey 是一款免费的浏览器扩展和最为流行的用户脚本管理器， 可以通过不同的“脚本”实现数十甚至上百个功能，比如视频去水印，去广告，js逆向定位加密参数生成位置等

安装：谷歌>右上角>更多工具>扩展程序，直接将crx文件拖入如下图页面
```

<img src="./img/1.png"></img>

#### @油猴脚本免费使用网站

```stylus
Userscript.Zone Search：是一个新网站，允许通过输入合适的URL或域来搜索用户脚本

Greasy Fork：最受欢迎的后起之秀，提供用户脚本的网站，可实现去掉视频播放广告，去水印等多种功能，可以直接安装使用，储存库中有大量的脚本资源

OpenUserJS：继 GreasyFork 之后开始创办，在其储存库中也拥有大量的脚本资源
```

#### @油猴脚本编写介绍

##### 第一步：添加脚本

```stylus
右上角打开油猴>添加新脚本>即为如下的编辑脚本页面
```

<img src="./img/2.png"></img>

<img src="./img/3.png"></img>

#### @油猴脚本注释内容解释

```stylus
@match这个注释的内容最为重要，它决定了你的脚本应用到哪个具体的网页，还是应用到所有的网页
    
@run-at确定了脚本的注入时机，在js逆向中也很重要

更多介绍:https://www.tampermonkey.net/documentation.php
```

| 属性名       | 作用                                                         |
| ------------ | ------------------------------------------------------------ |
| @name        | 油猴脚本的名字                                               |
| @namespace   | 命名空间，用来区分相同名称的脚本，一般写成作者名字或者网址就可以了 |
| @version     | 脚本版本，油猴脚本的更新会读取这个版本号                     |
| @description | 描述，用来告诉用户这个脚本是干什么用的                       |
| @author      | 作者名字                                                     |
| @match       | 只有匹配的网址才会执行对应的脚本，例如`*、http://*、http://www.baidu.com/*`等 |
| @grant       | 指定脚本运行所需权限，如果脚本拥有相应的权限，就可以调用油猴扩展提供的API与浏览器进行交互。如果设置为none的话，则不使用沙箱环境，脚本会直接运行在网页的环境中，这时候无法使用大部分油猴扩展的API。如果不指定的话，油猴会默认添加几个最常用的API |
| @require     | 如果脚本依赖其他js库的话，可以使用require指令，在运行脚本之前先加载其他库，常见用法是加载jquery，导库，和node差不多，相当于导入外部的脚本 |
| @run-at      | 脚本注入时机，这个比较重要，有时候是能不能hook到的关键，`document-start`：网页开始时；`document-body`：body出现时；`document-end`：载入时或者之后执行；`document-idle`：载入完成后执行，默认选项 |
| @connect     | 当用户使用GM_xmlhttpRequest请求远程数据的时候，需要使用connect指定允许访问的域名，支持域名、子域名、IP地址以及*通配符 |
| @updateURL   | 脚本更新网址，当油猴扩展检查更新的时候，会尝试从这个网址下载脚本，然后比对版本号确认是否更新 |

#### @编写油猴脚本的基本步骤

##### 编写到`// Your code here`那里即可

<img src="./img/4.png"></img>

#### @油猴脚本调试测试

```stylus
利用浏览器的调试功能，在脚本需要调试的地方添加debugger;语句，在相应网页刷新后，即可利用F12开发者工具进行单步调试、监视变量等操作了
```

<img src="./img/5.png"></img>



### 案例教程

```stylus
可用于：定位window属性加密参数，定位cookie生成位置、修改原函数等

借助油猴的hook：你可以将hook的脚本放到油猴里面执行

直接用谷歌控制台console界面进行hook：hook时机最好选择你看见的第一个js文件的第一行的时候下断点，然后在控制台console界面就注入

js hook 入门：https://www.52pojie.cn/forum.php?mod=viewthread&tid=1519457&extra=page%3D1%26filter%3Dtypeid%26typeid%3D378

hook深入理解:https://mp.weixin.qq.com/s/IYFyjVrVkHtUdCzn9arkJQ

更多探索：https://www.cnblogs.com/YuanEven/p/15719932.html
```

##### 1、hook之window属性案例

```stylus
（1）目标网站，目标定位加密参数pre：
```

<img src="./img/6.png"></img>

```stylus
（2）全局搜索’pre’参数，发现pre的值就是window._pt_的值，但是直接调试需要耗一些时间才能定位到加密位置，通过油猴hook可以轻松定位到加密位置
```

<img src="./img/7.png"></img>

```stylus
（3）首先，添加油猴脚本如下，保存该脚本并启用，然后切换到目标网页：
注意hook的域名为@match https://flight.qunar.com/*
hook的注入时机为文档开始时@run-at document-start
Object.defineProperty()：替换一个对象的属性，并返回此对象，属性里面可能存的是方法，也可能存的就是一个值（getter，setter）
而该脚本的hook点就是_pt_属性的get/set方法，在set处即_pt_属性被赋值时，debugger住
```

```javascript
// ==UserScript==
// @name         定位pre加密参数
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Shirmay1
// @run-at       document-start
// @match        https://flight.qunar.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var pre = "";
    Object.defineProperty(window, '_pt_', {
        get: function() {
            console.log('Getting window.属性');
            return pre
        },
        set: function(val) {
            console.log('Setting window.属性', val);
            debugger ;
            pre = val;
        }
    })
})();

```

```stylus
（4）接着，F12打开谷歌开发者工具，然后点击目标网站搜索按钮，油猴脚本随之执行，即可轻松定位到该加密参数位置，如下图
```

<img src="./img/8.png"></img>

```stylus
（5）最后，通过点击右侧调用栈回溯前一个函数，即可精准定位到window._pt_的值也就是pre的值
```

<img src="./img/9.png"></img>

##### 2、hook之cookie生成案例

```stylus
（1）目标网站：https://hotels.ctrip.com/hotel/shanghai2/star5#ctm_ref=ctr_hp_sb_lst，定位 _bfa这个cookie参数生成位置
```

<img src="./img/10.png"></img>

```stylus
（2）油猴脚本如下：test()检查字符串是否与给出的正则表达式模式相匹配，如果是则返回 true，否则就返回 false，该脚本匹配_bfa的相关字符串
```

```javascript
// ==UserScript==
// @name         定位携程cookie
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Shirmay1
// @match        https://hotels.ctrip.com/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var _cookie = document.cookie;; // hook cookie
    Object.defineProperty(document, 'cookie', {
        set: function(val) {
            console.log('cookie set->', val);
            var pi = new RegExp('^_bfa.*');
            if (pi.test(val)) {debugger;}
            _cookie = val;
            return val;
        },
        get: function() {
        	console.log('cookie get->', _cookie);
            return _cookie;
        }
   });
})();

```

#### @hook的脚本合集

① 简单的console界面直接hook，可如下

```javascript
Object.defineProperty(document, 'cookie', {
        set: function(val) {
            debugger ;
        }
    })

```

② 指定某个cookie简单的hook，如hook 这个cookie RM4hZBv0dDon443M

```javascript
Object.defineProperty(document, 'cookie', {
    set: function(val) {
        if (val.indexOf('RM4hZBv0dDon443M') != -1){
            debugger ;
        }
    }
})

```

③ 油猴脚本可如下设置： `hook所有cookie，注意修改@match 所匹配的网址，否则可能hook不到`

```javascript
// ==UserScript==
// @name         定位cookie
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Shirmay1
// @match        http://entp.yjj.gxzf.gov.cn/appnet/appEntpList.action?entpType=004
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function() {
   'use strict';
    var _cookie = ""; // hook cookie
    Object.defineProperty(document, 'cookie', {
        set: function(val) {
            console.log('cookie set->', new Date().getTime(), val);
            debugger;
            _cookie = val;
            return val;
        },
        get: function() {
            return _cookie;
        }
   });
})()

```

#### @hook之window属性

hook对象属性通用demo逻辑

<img src="./img/11.png"></img>

① 简单的console界面直接hook，window._$ss

```javascript
Object.defineProperty(window, '_$ss', {
    set: function(val) {
        debugger ;
    }
})

```

② 油猴脚本hook，window.*pt*

```javascript
// ==UserScript==
// @name         定位pre加密参数
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Shirmay1
// @run-at       document-start
// @match        https://flight.qunar.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var pre = "";
    Object.defineProperty(window, '_pt_', {
        get: function() {
            console.log('Getting window.属性');
            return pre
        },
        set: function(val) {
            console.log('Setting window.属性', val);
            debugger ;
            pre = val;
        }
    })
})();

```

#### @hook之eval

当检测函数的toString方法和原型链上的toString方法

```javascript
var _eval = eval
eval = function(arg) {
    debugger;
    return _eval(arg)
}
eval.toString = function() {
    return "function eval() { [native code] }"
}
eval.length = 1;
var _old = Function.prototype.toString.call
Function.prototype.toString.call = function(arg) {
    if (arg == eval)
        return "function eval() { [native code] }"
    return _old(arg);

}

```

#### @hook之setInterval

置空定时器或者过掉定时器的debugger

<img src="./img/12.png"></img>

```stylus
var _setInterval=setInterval;
setInterval=function(a,b){
	if(a.toString().indexOf("debugger")!=-1{
		return 
	}
	_setInterval(a,b);
}

```

#### @hook之console

<img src="./img/13.png"></img>

```stylus
console._log=console.log
console.log=function(a){
    if(a==="世上无难事，只要肯放弃"){
        return
    }
    console._log(a)
}

```

#### @hook函数中debugger

修改传参为debugger的函数，假设A函数有参数debugger传入

<img src="./img/14.png"></img>

```javascript
Function.prototype.constructor = function(param){
    if(param!="debugger"){
        return A(param)  
    }
    return function(){}
}

```

#### @hook之split

<img src="./img/15.png"></img>

```javascript
String.prototype.split_bk = String.prototype.split;
String.prototype.split = function(val){
    str =  this.toString();
    debugger;
    return str.split_bk(val)
}
a = 'dsdfasdf sdsasd'
a.split(' ')

```

#### @hook之Header

hook header中包含 Authorization 关键字

```stylus
(function () {
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        if (key == 'Authorization') {
            debugger;
        }
        return org.apply(this, arguments);
    };
})();

```

#### @hook之URL

hook url中包含login

```javascript
(function () {
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async) {
        if (url.indexOf("login") != -1) {
            debugger;
        }
        return open.apply(this, arguments);
    };
})();


```

#### @hook之JSON.stringify

```javascript
(function() {
    var stringify = JSON.stringify;
    JSON.stringify = function(params) {
        console.log("Hook JSON.stringify ——> ", params);
        debugger;
        return stringify(params);
    }
})();

```

#### @hook之JSON.parse

hook JSON.parse字符串转字典

```stylus
(function() {
    var parse = JSON.parse;
    JSON.parse = function(params) {
        console.log("Hook JSON.parse ——> ", params);
        debugger;
        return parse(params);
    }
})();

```

#### @hook之覆盖原函数总结

通用的函数hook覆盖demo逻辑

<img src="./img/16.png"></img>

（1）小案例，直接修改原函数

```javascript
function _before(){console.log("我是原函数执行中")}
var temp_before = _before;  // 原函数临时存储
_before = function(){console.log("我是原函数但被修改了")}
_before()  // 原函数被修改

```

（2）修改XMLHttpRequest.prototype.send，hook send

<img src="./img/17.png"></img>

（3）hook 原型对象返回字符串修改

```javascript
Function.prototype.toString=function(){
	return "function test(x,y){z=x+y;return z;}";
}

```

