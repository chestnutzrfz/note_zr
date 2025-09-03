# ast反混淆

##### 安装库

```
npm install @babel/node
```

##### 导包

```js
let parse = require("@babel/parser").parse
let generate = require("@babel/generator").default
let traverse = require("@babel/traverse").default
let types = require("@babel/types")
let fs = require('fs')

let js_code = fs.readFileSync('input.js','utf-8')
let ast = parse(js_code)




let decode_code = generate(ast).code
fs.writeFileSync('output.js',decode_code)
```

### 把一段js代码ast化 parse

```js
let ast = parse("var a=1;")
```

### 把ast代码变成js代码 generate

```js
let out_code = generate(ast).code
```

### ast遍历组件 traverse

```js
let {parse} = require("@babel/parser")
traverse = require("@babel/traverse").default
let ast = parse(`function hi(){console['\x6c\x6f\x67']('\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64\x21');}hi();`)

traverse(ast, { // 第二个参数是个对象
    StringLiteral: function(path){ // 需要遍历的ast type
// path 实际上是traverse的过程中，遍历的时候babel给我们传进去的一个对象，这个对象是构造函数 NodePath的实例化对象
		 exit: function (path){
            // exit: 出去的时候，再遍历，也就是可以理解为，从最深处往外边来
			// enter： 进去的时候遍历，也就是可以理解为，从最外边往深处去
            console.log(path.toString())
            let {confident,value} = path.evaluate();
            path.replaceInline({type:"NumericLiteral", value: value})
            console.log(confident, value)
        path.node.extra.raw = path.node.value
		// path.node 就是循环遍历的StringLiteral对象 可以直接用key取这个对象下面的value
         },		// 如果不改变ast内容的话  ,后可以写下一个
     }
})
```

##### ast 替换

```js
path.replaceInline(node)   // 里面自己定义node节点的type 等属性
path.replaceInline(types)    
// types 里面有很多很多可以创造各种node节点的方法 
types.valueToNode(x)    // 根据传入x的值创建需要的节点  可以使用该节点创建其他节点

let operator = path.get("value.body.body.0.argument").node.operator
let left = path.get("arguments.0").node
let right = path.get("arguments.1").node
path.replaceInline(types.binaryExpression(operator, left, right))
// 替换 操作符 左节点 右节点
```

##### scope

```
scope.path 就是拿到当前作用域块儿的path，
path.scope.path.toString()
path.scope.block 可以理解为是 path的Node。是作用域所在块的Node
path.scope.parent 就是返回上一级的作用域，也是一个 Scope对象
path.scope.parent.path.toString() // 当前这个再上一级就是全部了，它就没有 parent了
path.scope.bindings  返回一个 对象，这个对象的 key，就是变量名，value 是一个 Binding对象
path.scope.getAllBindings	返回当前作用域下所有binding
```

##### Binging

```
path.scope.bindings.g  里面有很多信息
referenced ---> 是否被引用
referencePaths 引用的path
references 引用次数
path  这个变量的path
identifier 这个变量的node
hasValue 是否有值
kind 变量类型，也可以理解为标识符类型 （参数 param/let/var/const）
constantViolations  标识符（变量名）如果被修改，会存到这个里面
hasValue 该绑定是否有值。（目前为止我用它都是设个标点，以便快速检索。）
我们也可以利用 path.scope.rename 去重命名所有的变量
也可以利用作用域的 path.scope.generateUidIdentifier("_0xabcdef") 来创建一个不重复的 Identifier

```



### path方法

| path方法                           | 方法介绍                                                     |
| ---------------------------------- | ------------------------------------------------------------ |
| path.node                          | 获取当前路径对应的节点。(Node的实例，没什么说的)             |
| path.get()                         | 这个可以理解为取 path路径下的path。 什么意思呢？ 就是说，path路径下正常如果取它的节点应该是path.node.argument,但是这样就会得到一个 node，没有办法再继续用 path的那些方法了但是如果我们 path.get("argument") ,就可以得到 path.node.argument 的path这里面，除了传字符串之外，还可以传得更复杂，比如说path.get("argument.0") |
| path.parent                        | 获取当前路径对应节点的父节点。（父节点，就是父节点）         |
| path.parentPath                    | 获取当前路径对应节点的父路径。（父路径，就是父节点的路径，是path属性，可以继续path操作） |
| path.scope                         | 表示当前path下的作用域，这个也是写插件经常会用到的。（scope里面事情比较多，下节课再聊） |
| path.container                     | 用于获取当前path下的所有兄弟节点(包括自身)。（其实就是数组，这个一会儿给大家演示） |
| path.type                          | 获取当前path的节点类型。（等于 path.node.type 没啥说的）     |
| path.key                           | 获取当前path的key值。 或者说是获取当前node 的key值           |
| path.getSibling(index)             | 获取当前路径对应节点的兄弟节点的路径。通过指定索引（index）可以获取相应的兄弟路径。 |
| path.getFunctionParent()           | 获取当前路径对应节点的最近的函数父节点的路径。               |
| path.getPrevSibling()              | 获取当前path的前一个兄弟节点，返回的是path类型。             |
| path.getAllPrevSiblings()          | 获取当前path的所有前兄弟节点，返回的是Array类型，其元素都是path类型。 |
| path.getNextSibling()              | 获取当前path的后一个兄弟节点，返回的是path类型。             |
| path.getAllNextSiblings()          | 获取当前path的所有后兄弟节点，返回的是Array类型，其元素都是path类型。 |
| path.evaluate()                    | 用于计算表达式的值。                                         |
| path.findParent()                  | 向上查找满足回调函数特征的path，即判断上级路径是否包含有XXX类型的节点。 |
| path.find()                        | 功能与 path.findParent 方法一样，只不过从当前path开始进行遍历。 |
| path.getFunctionParent()           | 获取函数类型父节点，如果不存在，返回 null。                  |
| path.getStatementParent()          | 获取Statement类型父节点，这个基本上都会有返回值，如果当前遍历的是 Program 或者 File 节点，则会报错。 |
| path.getAncestry()                 | 获取所有的祖先节点，没有实参，返回的是一个Array对象。        |
| path.isAncestor(maybeDescendant)   | 判断当前遍历的节点是否为实参的祖先节点.                      |
| path.isDescendant(maybeAncestor)   | 判断当前遍历的节点是否为实参的子孙节点.                      |
| path.traverse(visitor)             | 遍历当前路径下的所有子节点，并应用指定的 visitor。           |
| path.replaceWith(node)             | 用指定的节点替换当前路径对应的节点（单节点）                 |
| path.replaceWithMultiple(node)     | 用指定的节点替换当前路径对应的节点（多节点，也就是 [] 类型） |
| path.replaceWithSourceString(node) | 替换资源字符串（这个不太常用）                               |
| path.replaceInline(node)           | 兼容了 replaceWithMultiple 与 replaceWith，如果不考虑性能无脑用它就可以（对性能影响其实可以忽略不计） |
| path.remove()                      | 从 AST 中移除当前路径对应的节点。 // 个人的习惯和建议，删除放到最后在做 |
| path.insertBefore(nodes)           | 在当前路径对应节点之前插入一个或多个节点。                   |
| path.insertAfter(nodes)            | 在当前路径对应节点之后插入一个或多个节点。                   |
| path.insertAfter(nodes)            | 在当前路径对应节点之后插入一个或多个节点。                   |
| path.toString()                    | 用于将 AST 节点转换回对应的源代码字符串。                    |

##### generate 参数

```
generate可以传入三个参数
一个是AST语法树，第二个是配置。传入的是一个对象，第三个配置可以输出源代码，让程序进行参考

配置中比较常用的三个配置是：

retainLines  尝试输出代码中使用与源代码（第三个参数）一样的行号  默认 false
comments 输出结果是否包含注释  默认 true
minified 是否压缩输出  默认 false

其他配置
https://www.babeljs.cn/docs/babel-generator
```

##### traverse 参数

```
1. ast
2. 一个对象
{FunctionDeclaration: function(path){}}

这个对象的键除了可以输入遍历的节点类型之外， 还可以输入键： enter 和 exit

这两个表示的含义是，
enter：进入节点的操作
exit：退出节点的操作

所有的节点类型
https://github.com/babel/babel/blob/main/packages/babel-parser/ast/spec.md
```

##### demo

```js
let parse = require("@babel/parser").parse
let generate = require("@babel/generator").default
let traverse = require("@babel/traverse").default
let types = require("@babel/types")

let fs = require('fs')

let js_code = fs.readFileSync('input.js','utf-8')
let ast = parse(js_code)

var $a=['\x62\x38\x4f\x48\x77\x72\x6b\x3d','\x77\x70\x50\x43\x6a\x38\x4b\x2f','\x4a\x4d\x4b\x57\x53\x51\x3d\x3d','\x49\x33\x41\x55','\x56\x67\x58\x43\x6e\x77\x3d\x3d','\x43\x77\x33\x43\x6c\x77\x3d\x3d','\x77\x70\x62\x43\x6c\x73\x4f\x77','\x65\x73\x4b\x30\x4f\x51\x3d\x3d','\x77\x71\x44\x43\x69\x6e\x6b\x3d','\x53\x56\x68\x61','\x56\x73\x4b\x2f\x77\x34\x45\x3d','\x48\x44\x76\x43\x71\x67\x3d\x3d','\x48\x58\x72\x43\x6c\x51\x3d\x3d','\x41\x42\x6a\x43\x6e\x41\x3d\x3d','\x4b\x63\x4b\x39\x77\x72\x6b\x3d','\x59\x63\x4b\x41\x77\x35\x63\x3d','\x61\x73\x4b\x45\x5a\x41\x3d\x3d','\x63\x73\x4b\x6f\x77\x34\x55\x3d','\x43\x51\x4a\x57','\x77\x6f\x46\x41\x77\x6f\x41\x3d','\x47\x69\x62\x43\x6d\x51\x3d\x3d','\x45\x30\x37\x44\x73\x41\x3d\x3d','\x62\x63\x4b\x57\x52\x41\x3d\x3d','\x55\x69\x54\x44\x71\x41\x3d\x3d','\x55\x41\x6a\x44\x76\x41\x3d\x3d','\x77\x71\x66\x43\x6c\x63\x4f\x75','\x5a\x4d\x4b\x65\x62\x41\x3d\x3d','\x56\x53\x58\x43\x75\x41\x3d\x3d','\x4a\x4d\x4f\x53\x53\x51\x3d\x3d','\x4d\x30\x73\x54','\x77\x6f\x37\x43\x6b\x73\x4b\x72','\x4e\x73\x4b\x4b\x77\x71\x63\x3d','\x64\x63\x4b\x74\x4f\x41\x3d\x3d','\x35\x62\x2b\x6f\x4b\x33\x6f\x3d','\x50\x52\x4d\x42','\x4c\x63\x4b\x6a\x77\x71\x45\x3d','\x35\x62\x2b\x59\x77\x71\x76\x44\x72\x41\x3d\x3d','\x58\x53\x54\x44\x75\x77\x3d\x3d','\x77\x6f\x6a\x43\x6e\x57\x34\x3d','\x49\x54\x42\x43','\x35\x4c\x6d\x33\x35\x35\x61\x6e\x36\x49\x69\x51','\x77\x34\x45\x56\x45\x67\x3d\x3d','\x53\x63\x4b\x75\x4a\x67\x3d\x3d','\x77\x71\x51\x4f\x77\x6f\x77\x3d','\x4b\x4d\x4f\x5a\x77\x70\x59\x3d','\x77\x6f\x55\x38\x77\x70\x67\x3d','\x4f\x43\x6b\x77','\x77\x72\x30\x2f\x77\x34\x38\x3d','\x4c\x63\x4b\x69\x77\x6f\x41\x3d','\x59\x54\x38\x4c','\x4c\x38\x4b\x31\x57\x41\x3d\x3d','\x77\x36\x51\x46\x42\x41\x3d\x3d','\x77\x70\x4c\x43\x6e\x4d\x4f\x6e','\x53\x54\x50\x43\x76\x41\x3d\x3d','\x64\x42\x50\x43\x6f\x41\x3d\x3d','\x46\x6d\x6e\x43\x73\x77\x3d\x3d','\x50\x38\x4f\x67\x49\x67\x3d\x3d','\x59\x6a\x67\x62','\x77\x34\x6f\x64\x4c\x67\x3d\x3d','\x41\x63\x4b\x64\x77\x72\x59\x3d','\x4f\x38\x4f\x45\x77\x6f\x59\x3d','\x77\x72\x54\x43\x75\x63\x4f\x30','\x43\x78\x78\x43','\x61\x4d\x4f\x6f\x77\x72\x38\x3d','\x46\x73\x4b\x46\x77\x72\x34\x3d','\x77\x36\x37\x43\x76\x73\x4b\x73','\x62\x78\x76\x43\x6b\x41\x3d\x3d','\x54\x73\x4f\x73\x77\x37\x77\x3d','\x77\x72\x37\x43\x73\x38\x4b\x69','\x77\x72\x6e\x43\x68\x63\x4b\x36','\x77\x6f\x62\x44\x76\x4d\x4b\x35','\x4e\x38\x4b\x45\x56\x51\x3d\x3d','\x77\x6f\x6e\x43\x68\x38\x4f\x69','\x53\x79\x58\x43\x6c\x51\x3d\x3d','\x57\x38\x4b\x6d\x4b\x51\x3d\x3d','\x77\x6f\x50\x43\x6b\x4d\x4b\x63','\x77\x70\x78\x43\x61\x41\x3d\x3d','\x41\x38\x4b\x6d\x77\x37\x41\x3d','\x35\x35\x2b\x66\x37\x37\x2b\x57\x35\x4c\x2b\x56','\x63\x51\x50\x44\x70\x67\x3d\x3d','\x58\x78\x4c\x43\x75\x41\x3d\x3d','\x77\x70\x44\x43\x74\x56\x63\x3d','\x65\x4d\x4b\x4a\x77\x34\x55\x3d','\x48\x67\x76\x43\x6a\x41\x3d\x3d','\x77\x71\x4c\x43\x6c\x4d\x4f\x31','\x52\x43\x54\x44\x6c\x41\x3d\x3d','\x49\x69\x39\x64','\x77\x6f\x44\x43\x68\x63\x4f\x74','\x50\x67\x33\x43\x6a\x77\x3d\x3d','\x77\x37\x2f\x43\x67\x73\x4f\x73','\x77\x6f\x2f\x43\x6e\x55\x34\x3d','\x48\x54\x4a\x35','\x55\x41\x2f\x43\x68\x51\x3d\x3d','\x62\x44\x58\x43\x6c\x51\x3d\x3d','\x77\x70\x2f\x43\x76\x31\x59\x3d','\x77\x72\x44\x43\x6c\x4d\x4f\x53','\x77\x35\x48\x43\x6e\x38\x4f\x4a','\x77\x72\x6a\x43\x6e\x38\x4f\x4b','\x4b\x47\x48\x43\x6f\x67\x3d\x3d','\x77\x6f\x6a\x43\x67\x63\x4b\x61','\x61\x54\x33\x43\x6a\x41\x3d\x3d','\x77\x72\x72\x43\x76\x4d\x4f\x6f','\x4c\x4d\x4b\x77\x53\x67\x3d\x3d','\x4e\x63\x4b\x4e\x57\x41\x3d\x3d','\x77\x6f\x45\x48\x77\x36\x51\x3d','\x4c\x63\x4f\x71\x77\x71\x63\x3d','\x4f\x6b\x33\x43\x71\x67\x3d\x3d','\x49\x32\x58\x43\x73\x67\x3d\x3d','\x77\x71\x44\x43\x6f\x38\x4f\x72','\x77\x35\x76\x43\x67\x73\x4b\x79','\x5a\x38\x4b\x69\x49\x67\x3d\x3d','\x50\x44\x72\x43\x6a\x77\x3d\x3d','\x77\x35\x30\x4f\x77\x35\x30\x3d','\x65\x4d\x4f\x37\x77\x37\x4d\x3d','\x77\x35\x67\x73\x41\x77\x3d\x3d','\x49\x38\x4f\x6f\x51\x77\x3d\x3d','\x51\x4d\x4b\x51\x49\x77\x3d\x3d','\x56\x43\x30\x31','\x65\x42\x6b\x31','\x77\x36\x59\x31\x77\x36\x59\x3d','\x77\x35\x77\x76\x4c\x51\x3d\x3d','\x77\x71\x6e\x43\x6b\x38\x4f\x36','\x50\x79\x56\x30','\x77\x35\x77\x31\x47\x41\x3d\x3d','\x61\x38\x4b\x42\x77\x36\x30\x3d','\x77\x70\x62\x43\x6f\x46\x55\x3d','\x62\x43\x34\x59','\x52\x38\x4b\x37\x54\x51\x3d\x3d','\x77\x72\x41\x42\x77\x70\x41\x3d','\x77\x70\x44\x43\x73\x63\x4f\x2f','\x44\x38\x4b\x39\x77\x71\x73\x3d','\x50\x63\x4b\x72\x66\x41\x3d\x3d','\x49\x6e\x51\x39','\x77\x70\x6a\x43\x75\x6e\x6f\x3d','\x52\x6a\x74\x4f','\x77\x34\x48\x43\x72\x73\x4f\x66','\x58\x77\x6e\x44\x74\x77\x3d\x3d','\x45\x38\x4f\x34\x77\x72\x63\x3d','\x77\x6f\x76\x43\x76\x38\x4f\x59','\x63\x4d\x4b\x59\x77\x37\x30\x3d','\x64\x38\x4f\x45\x77\x70\x59\x3d','\x65\x54\x54\x43\x6e\x41\x3d\x3d','\x45\x69\x66\x43\x6e\x51\x3d\x3d','\x4b\x38\x4b\x4b\x4a\x41\x3d\x3d','\x66\x41\x6b\x66','\x77\x6f\x30\x67\x77\x6f\x38\x3d','\x47\x79\x33\x43\x67\x77\x3d\x3d','\x41\x51\x41\x37','\x52\x78\x76\x44\x76\x77\x3d\x3d','\x77\x6f\x50\x43\x6b\x38\x4b\x69','\x77\x6f\x6b\x6a\x59\x51\x3d\x3d','\x51\x63\x4f\x68\x77\x72\x41\x3d','\x77\x71\x68\x44\x77\x71\x4d\x3d','\x56\x63\x4b\x75\x77\x36\x67\x3d','\x77\x34\x4d\x6f\x46\x77\x3d\x3d','\x62\x43\x6e\x44\x73\x51\x3d\x3d','\x63\x55\x46\x74','\x53\x30\x62\x44\x75\x77\x3d\x3d','\x45\x73\x4b\x44\x77\x70\x59\x3d','\x77\x72\x62\x43\x6d\x63\x4f\x58','\x4e\x78\x46\x7a','\x53\x53\x35\x6c','\x77\x72\x62\x43\x6c\x63\x4b\x58','\x77\x72\x54\x43\x70\x33\x34\x3d','\x4c\x4d\x4b\x6a\x46\x51\x3d\x3d','\x54\x57\x74\x46','\x61\x68\x66\x43\x68\x51\x3d\x3d','\x77\x70\x50\x43\x74\x46\x77\x3d','\x77\x37\x30\x6b\x4d\x77\x3d\x3d','\x41\x51\x54\x43\x6e\x51\x3d\x3d','\x77\x35\x72\x43\x72\x4d\x4f\x63','\x77\x71\x51\x2f\x77\x72\x55\x3d','\x41\x63\x4b\x7a\x77\x72\x51\x3d','\x77\x70\x37\x43\x73\x56\x34\x3d','\x62\x47\x64\x68','\x62\x44\x42\x35','\x77\x34\x66\x43\x68\x4d\x4f\x41','\x61\x38\x4f\x6f\x77\x71\x59\x3d','\x77\x71\x63\x6e\x77\x70\x4d\x3d','\x55\x38\x4b\x51\x77\x35\x6b\x3d','\x45\x77\x78\x57','\x65\x63\x4f\x65\x77\x6f\x51\x3d','\x77\x36\x30\x45\x4f\x77\x3d\x3d','\x53\x51\x34\x6b','\x4b\x69\x63\x34','\x55\x38\x4b\x6f\x77\x34\x4d\x3d','\x54\x38\x4b\x53\x77\x36\x41\x3d','\x65\x63\x4b\x4e\x4e\x51\x3d\x3d','\x57\x63\x4f\x4d\x77\x71\x4d\x3d','\x45\x7a\x33\x43\x6a\x67\x3d\x3d','\x77\x71\x56\x6c\x77\x72\x51\x3d','\x77\x36\x72\x43\x6d\x38\x4b\x47','\x4a\x68\x30\x32','\x77\x71\x62\x43\x73\x4d\x4b\x67','\x77\x71\x58\x43\x6e\x73\x4b\x36','\x77\x71\x44\x43\x6e\x4d\x4f\x58','\x77\x6f\x44\x43\x72\x4d\x4f\x4b','\x49\x51\x55\x31','\x43\x38\x4b\x4b\x77\x6f\x51\x3d','\x77\x72\x37\x43\x6d\x6e\x67\x3d','\x4e\x54\x4a\x39','\x77\x35\x48\x43\x6f\x73\x4f\x4b','\x77\x6f\x73\x42\x77\x71\x59\x3d','\x57\x68\x63\x49','\x77\x6f\x33\x43\x67\x63\x4f\x70','\x55\x6a\x66\x44\x70\x67\x3d\x3d','\x77\x71\x7a\x44\x73\x73\x4b\x35','\x77\x72\x6f\x5a\x77\x71\x6f\x3d','\x50\x73\x4b\x70\x43\x67\x3d\x3d','\x77\x71\x30\x52\x4a\x77\x3d\x3d','\x77\x37\x73\x75\x4f\x67\x3d\x3d','\x77\x71\x73\x73\x4a\x67\x3d\x3d','\x77\x70\x33\x43\x6f\x6e\x6f\x3d','\x47\x73\x4f\x66\x77\x6f\x51\x3d','\x77\x72\x64\x6b\x77\x71\x77\x3d','\x42\x63\x4f\x64\x77\x70\x67\x3d','\x42\x6e\x63\x42','\x65\x63\x4b\x50\x53\x51\x3d\x3d','\x77\x71\x41\x39\x49\x41\x3d\x3d','\x4a\x4d\x4b\x31\x63\x67\x3d\x3d','\x4a\x38\x4f\x32\x57\x77\x3d\x3d','\x77\x72\x6e\x43\x69\x33\x49\x3d','\x56\x63\x4b\x77\x4a\x77\x3d\x3d','\x63\x63\x4b\x71\x4e\x77\x3d\x3d','\x77\x71\x7a\x43\x68\x63\x4f\x69','\x46\x68\x37\x43\x67\x41\x3d\x3d','\x77\x36\x6f\x7a\x42\x51\x3d\x3d','\x77\x71\x6e\x43\x73\x73\x4f\x52','\x77\x36\x55\x4b\x77\x37\x6b\x3d','\x77\x72\x62\x43\x72\x63\x4b\x4e','\x41\x73\x4b\x6d\x77\x72\x51\x3d','\x77\x71\x34\x56\x41\x67\x3d\x3d','\x66\x43\x7a\x43\x6c\x77\x3d\x3d','\x66\x63\x4b\x70\x77\x6f\x38\x3d','\x77\x6f\x45\x63\x47\x67\x3d\x3d','\x4a\x63\x4f\x74\x53\x51\x3d\x3d','\x77\x70\x76\x43\x6f\x38\x4f\x48','\x77\x71\x72\x43\x6e\x38\x4f\x30','\x53\x38\x4b\x7a\x4c\x67\x3d\x3d','\x77\x6f\x37\x43\x6b\x4d\x4b\x4d','\x4b\x4d\x4f\x46\x77\x6f\x63\x3d','\x4f\x73\x4b\x46\x4f\x51\x3d\x3d','\x56\x7a\x62\x43\x71\x41\x3d\x3d','\x61\x4d\x4b\x4b\x77\x37\x49\x3d','\x77\x72\x58\x43\x70\x6e\x49\x3d','\x44\x67\x5a\x79','\x4a\x51\x39\x44','\x77\x71\x6e\x44\x6c\x4d\x4b\x56','\x41\x7a\x6e\x43\x71\x51\x3d\x3d','\x48\x4d\x4b\x58\x63\x41\x3d\x3d','\x52\x4d\x4b\x55\x77\x35\x63\x3d','\x77\x6f\x66\x43\x72\x63\x4b\x52','\x4f\x63\x4f\x4c\x53\x51\x3d\x3d','\x77\x34\x54\x43\x70\x4d\x4b\x64','\x44\x54\x54\x43\x6f\x77\x3d\x3d','\x48\x41\x70\x50','\x77\x71\x70\x63\x77\x6f\x73\x3d','\x61\x73\x4b\x2b\x54\x51\x3d\x3d','\x77\x36\x6f\x57\x42\x41\x3d\x3d','\x35\x35\x79\x34\x37\x37\x32\x47\x35\x4c\x2b\x31'];
(function(a,b){var c=function(g){while(--g){a['push'](a['shift']());}};var f=function(){var g={'data':{'key':'cookie','value':'timeout'},'setCookie':function(k,l,m,n){n=n||{};var o=l+'='+m;var p=0x0;for(var q=0x0,r=k['length'];q<r;q++){var s=k[q];o+=';\x20'+s;var t=k[s];k['push'](t);r=k['length'];if(t!==!![]){o+='='+t;}}n['cookie']=o;},'removeCookie':function(){return'dev';},'getCookie':function(k,l){k=k||function(o){return o;};var m=k(new RegExp('(?:^|;\x20)'+l['replace'](/([.$?*|{}()[]\/+^])/g,'$1')+'=([^;]*)'));var n=function(o,p){o(++p);};n(c,b);return m?decodeURIComponent(m[0x1]):undefined;}};var h=function(){var k=new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');return k['test'](g['removeCookie']['toString']());};g['updateCookie']=h;var i='';var j=g['updateCookie']();if(!j){g['setCookie'](['*'],'counter',0x1);}else if(j){i=g['getCookie'](null,'counter');}else{g['removeCookie']();}};f();}($a,0x152));var $b=function(a,b){a=a-0x0;var c=$a[a];if($b['zOuuZS']===undefined){(function(){var f;try{var h=Function('return\x20(function()\x20'+'{}.constructor(\x22return\x20this\x22)(\x20)'+');');f=h();}catch(i){f=window;}var g='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';f['atob']||(f['atob']=function(j){var k=String(j)['replace'](/=+$/,'');var l='';for(var m=0x0,n,o,p=0x0;o=k['charAt'](p++);~o&&(n=m%0x4?n*0x40+o:o,m++%0x4)?l+=String['fromCharCode'](0xff&n>>(-0x2*m&0x6)):0x0){o=g['indexOf'](o);}return l;});}());var e=function(f,g){var h=[],l=0x0,m,n='',o='';f=atob(f);for(var q=0x0,r=f['length'];q<r;q++){o+='%'+('00'+f['charCodeAt'](q)['toString'](0x10))['slice'](-0x2);}f=decodeURIComponent(o);var p;for(p=0x0;p<0x100;p++){h[p]=p;}for(p=0x0;p<0x100;p++){l=(l+h[p]+g['charCodeAt'](p%g['length']))%0x100;m=h[p];h[p]=h[l];h[l]=m;}p=0x0;l=0x0;for(var t=0x0;t<f['length'];t++){p=(p+0x1)%0x100;l=(l+h[p])%0x100;m=h[p];h[p]=h[l];h[l]=m;n+=String['fromCharCode'](f['charCodeAt'](t)^h[(h[p]+h[l])%0x100]);}return n;};$b['AhcVNV']=e;$b['cECssq']={};$b['zOuuZS']=!![];}var d=$b['cECssq'][a];if(d===undefined){if($b['jtrmxJ']===undefined){var f=function(g){this['XEzqLf']=g;this['bRMhJj']=[0x1,0x0,0x0];this['mCmNwn']=function(){return'newState';};this['qseWjg']='\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*';this['uSohKm']='[\x27|\x22].+[\x27|\x22];?\x20*}';};f['prototype']['wESivq']=function(){var g=new RegExp(this['qseWjg']+this['uSohKm']);var h=g['test'](this['mCmNwn']['toString']())?--this['bRMhJj'][0x1]:--this['bRMhJj'][0x0];return this['dYPDiE'](h);};f['prototype']['dYPDiE']=function(g){if(!Boolean(~g)){return g;}return this['zAMxec'](this['XEzqLf']);};f['prototype']['zAMxec']=function(g){for(var h=0x0,j=this['bRMhJj']['length'];h<j;h++){this['bRMhJj']['push'](Math['round'](Math['random']()));j=this['bRMhJj']['length'];}return g(this['bRMhJj'][0x0]);};new f($b)['wESivq']();$b['jtrmxJ']=!![];}c=$b['AhcVNV'](c,b);$b['cECssq'][a]=c;}else{c=d;}return c;};

// 1. 将$b 中的字符串 替换为 执行$b()后得到的值  方便查看
traverse(ast,{
    CallExpression: function (path){
        if(path.node.callee.name === '$b'){
            // console.log(path.toString())
            path.replaceWith({
                type: "StringLiteral",
                value: $b(path.node.arguments[0].value,path.node.arguments[1].value)
            })
        }
    }
})
// 2. 还原 对象中简单的字符串  type: MemberExpression
traverse(ast,{
    BinaryExpression: {
        exit: function (path) {
            let left = path.get("left").node.value
            let right = path.get("right").node.value
            if (path.get("left").isStringLiteral() && path.get("right").isStringLiteral()) {
                path.replaceInline(types.valueToNode(left + right))
            }
        }
    }
})
let remove_list = []
// 3. 还原花指令     函数的还原           字符串的还原
traverse(ast,{
    CallExpression:{
        exit: function (path){
            if(path.get('callee.object').node && ["A", "a7", "a3"].includes(path.get("callee.object").node.name)){
                let property = path.get("callee.property").node.value   // YdYIz
                remove_list.push(property)
                let argument_path_array = path.get("arguments")     // 参数
                // 还原
                path.scope.getBinding(path.get('callee.object').node.name).scope.path.traverse({
                    AssignmentExpression: function (path_Expression){     // 每个函数
                        if(path_Expression.get('left').isMemberExpression()){
                            if(path_Expression.get('left.property').node && path_Expression.get('left.property').node.value === property){
                                let return_path = path_Expression.get('right.body.body.0.argument')
                                // console.log(return_path)
                                if(return_path.isBinaryExpression()){
                                    let left = argument_path_array[0].node
                                    let operator = return_path.node.operator
                                    let right = argument_path_array[1].node
                                    path.replaceInline(types.binaryExpression(operator,left,right))
                                }
                                else if(return_path.isCallExpression()){
                                    let function_path = argument_path_array[0].node
                                    let function_arguments = path.node.arguments.slice(1)
                                    // console.log(function_arguments)
                                    path.replaceInline(types.CallExpression(function_path,function_arguments))
                                }
                            }
                        }
                    }
                })
            }
        }
    }
})
// 字符串的还原    y["GJYeW"] = "return /\" + this + \"/";
traverse(ast,{
    MemberExpression: function (path){
        if(["A", "a7", "a3"].includes(path.get("object.name").node) && path.get('property').node.type === 'StringLiteral'){
            // console.log(path.toString())
            let _string  = path.get('property').node.value
            path.scope.getBinding(path.get('object.name').node).scope.path.traverse({
                AssignmentExpression: function (path_assign) {
                    if(path_assign.get('right').node.type === 'StringLiteral' && path_assign.get('left.property').node.value === _string){
                        path.replaceInline(types.valueToNode(path_assign.get('right').node.value))
                        remove_list.push(path_assign.get('left.property').node.value)
                    }
                }
            })
        }
    }
})
// 控制流平坦化
let b = "0|5|6|3|4|2|1"["split"]('|');
let control = []    // 控制流的代码依次存入

traverse(ast,{
    SwitchCase: function (path){
        control[path.get("test.value").node] = path.node.consequent.slice(0, path.get("consequent").length-1)
    }
})
// console.log(control)
// 控制流平坦化  替换while
traverse(ast,{
    WhileStatement: function (path){
        if(!path.get("body.body.0").isSwitchStatement()){
            return
        }
        let new_code = ""
        for(let i of b){
            new_code += control[i]
        }
        // console.log(new_code)
        // parse(new_code)
        path.replaceInline(parse(new_code))
    }
})
// 删除无用代码
// console.log(remove_list)
traverse(ast,{
    AssignmentExpression: function (path){
        for(let i of remove_list){
            if(path.get('left.property').node && path.get('left.property').node.value === remove_list[i]){
                console.log(i)
                console.log(path.scope.getAllBindings())
                // 没找明白
                process.exit()
            }
        }
    }
})




let decode_code = generate(ast).code
fs.writeFileSync('output.js',decode_code)

```

##### 复杂控制流平坦化

```js
let parse = require("@babel/parser").parse
let generate = require("@babel/generator").default
let traverse = require("@babel/traverse").default
let types = require("@babel/types")
let fs = require('fs')

let js_code = fs.readFileSync('input.js', 'utf-8')
let ast = parse(js_code)

/*疯狂找规律（一定要耐心，因为混淆也是规律混淆，所以我们反混淆也是找规律反混）
1.  if 的 else 如果没有继续承接 if，那else 等于 if 判断右边的值
    举例： if (f < 5) {if(f < 4)...} else {...}
    else 里面没有直接承接  else{if(f.....)}, 所以 else 实际上就是 f -----> case 4
2.  对于  if 里面直接没有承接的情况
    例  if (f < 7) {...} else {...}
    一直找祖宗节点，直到找到 第一次的else 分支的 if，这个 if 判断右边的值 就是 case 的值  实际 f的值
3.  使用 enter 还是 exit
4.  如何替换掉节点与中间变量的存储*/


// 准备工作  for(;;) 后没有{}  可以添加一个 块级作用域  更方便
traverse(ast, {
    ForStatement: function (path) {
        path.node.body = types.blockStatement([path.node.body])
    }
})

// 第一步 还原简易 else
traverse(ast, {
    IfStatement: {
        exit: function (path) {
            // if 下面有else节点  节点里有内容  节点里没有if
            if (path.get('alternate').node && path.get('alternate.body').length && !path.get('alternate.body.0').isIfStatement()) {
                let name = path.get('test').node.left.name
                let value = path.get('test').node.right.value
                // 创建if(i===x){xxxx} 的节点且放for循环前面 用types
                let test = types.BinaryExpression('===', types.Identifier(name), types.valueToNode(value))
                let consequent = path.get('alternate').node    // else节点整个块
                let unshift_node = types.IfStatement(test, consequent)  // 把else节点整个的块放到新创建的if节点后
                // 根据name拿到path 路径下的绑定节点    拿父节点下面的兄弟节点的第二个节点  (最开始的for(;;) 循环位置) 在其body (就是循环后的{}) 里面用unshift将新创建的节点放到最前面
                path.scope.getBinding(name).path.parentPath.container[1].body.body.unshift(unshift_node)
                path.get("alternate").remove()
            }
        }
    }
})
// 第二步 还原简易的if
traverse(ast, {
    IfStatement: {
        exit: function (path) {
            // if 下面有else节点  节点里有内容  节点里没有if
            if (path.get('consequent').node && path.get('consequent.body').length && !path.get('consequent.body.0').isIfStatement()) {
                if (path.get('test.operator').node === '<') {
                    if (path.get('test.right.value').node === 1) {
                        var value = 0;
                        var name = path.get('test').node.left.name
                    } else {
                        let _path = path
                        while (1) { // 一直死循环找父节点  一直找到key 是else的时候停下来
                            if (_path.parentPath.key === "alternate") {
                                var name = _path.parentPath.parentPath.get("test").node.left.name
                                var value = _path.parentPath.parentPath.get("test").node.right.value
                                break
                            }
                            _path = _path.parentPath;
                        }
                    }
                    var test = types.binaryExpression("===", types.Identifier(name), types.valueToNode(value));
                    var consequent = path.get("consequent").node;
                    path.scope.getBinding(name).path.parentPath.container[1].body.body.unshift(types.IfStatement(test, consequent))
                    path.get("consequent").remove()
                }
            }
        }
    }
})
// 第三步 删除垃圾代码     判断if里面有没有值  没有就删掉
traverse(ast, {
    IfStatement: {
        exit: function (path) {
            // console.log(path.toString())
            if (path.get("consequent.body") && path.get("consequent.body").length === 0) {
                if (!path.get("alternate").node || path.get("alternate.body").length === 0) {
                    path.remove()
                }
            }
        }
    }
})
// 满满恶意之插桩优化   for循环的分支  中没有continue 导致执行的循环没有按照预想去插桩  第一次运行得到插桩结果后 注释掉防止报错
// traverse(ast, {
//     ExpressionStatement: function (path) {
//         let grand_node_path = path.parentPath.parentPath
//         if (grand_node_path && grand_node_path.isIfStatement() && grand_node_path.get("test.left.name").node === "f") {
//             if (path.get('expression.left').node && path.get("expression.left.name").node === "f") {
//                 // path.parentPath.node.body.push(types.ContinueStatement())
//                 path.insertAfter(types.ContinueStatement()) // 添加continue
//             }
//         }
//     }
// })
// 在浏览器中执行js代码   确保环境没问题   插桩 得到 执行流程
let _f = [
    12, 4, 15, 0, 22, 16, 10, 25,
    26, 5, 1, 23, 6, 8, 13, 14,
    9, 2, 21, 7, 18, 19, 11, 3,
    20, 24, 17
];
// 控制流平坦化
let _f_code = [];
traverse(ast, {
    ForStatement: function (path) {
        for (i of _f) {
            path.traverse({
                IfStatement: function (_ifPath) {
                    if (_ifPath.get("test.left.name").node === "f" && _ifPath.get("test.right.value").node === i) {
                        _f_code.push.apply(_f_code, _ifPath.get("consequent").node.body)
                    }
                }
            })
        }
        path.parentPath.node.body.push.apply(path.parentPath.node.body, _f_code)
        path.remove()
        return 0
    }
})


let decode_code = generate(ast).code
fs.writeFileSync('output.js', decode_code)

/*
未完全完成
还有 s l i 的控制流没有完成
f += 1;  这样的运算也无用了可以删除
流程是相同的
还有无用代码的删除
*/

```

