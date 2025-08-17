### ob混淆

ob混淆    开源http://obfuscator.io/

一般都是依靠ob开源框架并且增加了自己的一些理解的加壳器



大数组

数组移位

解密函数



##### 解ob混淆的正则表达式造成的浏览器卡死

```js
RegExp.prototype.test = function (){
    return true
}
```

