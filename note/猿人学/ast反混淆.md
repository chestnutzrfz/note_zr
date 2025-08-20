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


let memory = {}
// 第一步 将 a对象中的值放入内存    直接复制 a对象也行
traverse(ast,{
    VariableDeclarator: function (path){
        if(["a", "b", "e", "f"].indexOf(path.node.id.name) !== -1){
            if(path.get("init").type === "ObjectExpression"){
                eval(path.toString())
                memory[path.get("id").node.name] = path
            }
        }
    }
})
// 第二步 还原 a对象中简单的字符串  type: MemberExpression
traverse(ast,{
    MemberExpression: function (path){
        if(["a", "b", "e", "f"].indexOf(path.get('object').node.name) !== -1 && path.get('property').type === 'StringLiteral'){
            // console.log(path.toString())
            let result = eval(path.toString())
            if(typeof result === 'string'){
                path.replaceInline({type:"StringLiteral", value: result})
            }
        }
    }
})
// 第三步 还原控制流平坦化 part1 取控制流的代码
var b = "4|2|1|6|3|7|5|8|0"["split"]('|');
var control = []    // 控制流的代码依次存入

traverse(ast,{
    SwitchCase: function (path){
        control[path.get('test.value').node] = path.get('consequent.0').toString()
    }
})
// console.log(control)
// 第三步 还原控制流平坦化 part2 替换while
traverse(ast,{
    WhileStatement: function (path){
        let new_code = ""
        for(let i of b){
            new_code += control[i]
        }
        path.replaceInline(parse(new_code))
    }
})
// 第四步 还原a 中的函数
traverse(ast,{
    CallExpression: {
        exit: function (path){
            if(path.get("callee.object").node && ["a", "b", "e", "f"].indexOf(path.get("callee.object").node.name) !== -1){
                //    第一种是函数执行， 第二种是操作符计算
                for (let i of memory[path.get("callee.object").node.name].get("init.properties")) {
                    if (path.get("callee").node && path.get("callee.property").node && i.node.key.value === path.get("callee.property").node.value) {
                        // 操作符
                        if (i.get("value.body.body.0.argument").type === "BinaryExpression") {
                            let operator = i.get("value.body.body.0.argument").node.operator
                            let left = path.get("arguments.0").node
                            let right = path.get("arguments.1").node
                            path.replaceInline(types.binaryExpression(operator, left, right))
                        }
                        // 函数
                        else if (i.get("value.body.body.0.argument").type === "CallExpression") {
                            // console.log(path.toString())
                            let function_path = path.get("arguments.0").node
                            let function_arguments = path.node.arguments.slice(1)
                            // console.log(function_arguments.length)
                            path.replaceInline(types.callExpression(function_path, function_arguments))
                            // console.log(i.get("value.body.body.0.argument").toString())
                        }
                    }
                }
            }
        }
    }
})
// 第五步 删除无效代码
traverse(ast, {
    VariableDeclarator: function (path){
        if(["a", "b", "e", "f"].indexOf(path.get("id").node.name) !== -1){   // 或者 path.get("id.name").node === "a"
            if(path.get("init").type === "ObjectExpression"){
                // eval(path.toString())
                // memory[path.get("id").node.name] = path
                path.remove()
            }
        }
    },
})

let decode_code = generate(ast).code
fs.writeFileSync('output.js',decode_code)


```

