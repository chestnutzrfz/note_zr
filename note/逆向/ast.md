# AST反混淆

### AST 简单语法

##### 导包

```js
let parse = require("@babel/parser").parse
let generate = require("@babel/generator").default
let traverse = require("@babel/traverse").default
```

##### 转换AST

```js
// 把js代码 抽象成 抽象语法树
let ast = parse("var a=1;")
// 把 转换成的抽象语法树 转换回js代码
let out_code = generate(ast).code
```

##### 转换结果

```js
// var a=1;  抽象成 ast的代码
Node {	// 第一层
  type: 'File',
  start: 0,	// 字符串的起始位置
  end: 8,	// 结束位置
  loc: SourceLocation {	// 行和列的信息
    start: Position { line: 1, column: 0, index: 0 },
    end: Position { line: 1, column: 8, index: 8 },
    filename: undefined,
    identifierName: undefined
  },
  errors: [],	// 错误解析的数组
  program: Node {	// 第二层 核心部分 包含代码的AST节点
    type: 'Program',	// js源代码主体
    start: 0,	// 起始
    end: 8,		// 结束
    loc: SourceLocation {
      start: [Position],
      end: [Position],
      filename: undefined,
      identifierName: undefined
    },
    sourceType: 'script',
    interpreter: null,
    body: [ [Node] ],	// 第三层 关键数组, 包含顶级语法节点
    directives: []
  },
  comments: []	// 注释数组
}
```

##### 树的结构

```less
File
└─ Program
   └─ body[0] : VariableDeclaration (kind: var)
      └─ declarations[0] : VariableDeclarator
         ├─ id : Identifier (name: "a")
         └─ init : NumericLiteral (value: 1)
// VariableDeclaration 声明变量 变量说明符
```

##### tarverse 语法

```
是 AST 关键部分  Babel 遍历AST语法 

traverse(ast, visitor)
ast 转换得到的 语法树
visitor 一个对象,定义了想访问的节点类型以及对应回调函数

path 表示当前遍历到的AST节点的路径对象
path 包含了节点本身, 父节点, 作用域信息等
可以用path 安全地修改节点, 替换节点, 删除节点等

具体回调函数 
path.node.extra.raw = path.node.value
path.node.value 是字面量的真实值
path.node.extra.raw 是Babel AST节点中保存原始源码文本的地方  保留原始引号和转义
可以转换 \xff 清理混淆输出,让字符串变回可读形式
```

```js
traverse(ast, {
    StringLiteral: function(path){
        path.node.extra.raw = path.node.value
    }
})
// StringLiteral 字符串字面量
```

##### path语法

```
path.node	获取当前路径对应的节点。（Node的实例，没什么说的）
path.parent	获取当前路径对应节点的父节点。（父节点，就是父节点）
path.parentPath	获取当前路径对应节点的父路径。（父路径，就是父节点的路径，是path属性，可以继续path操作）
path.scope	表示当前path下的作用域，这个也是写插件经常会用到的。（scope里面事情比较多，下节课再聊）
path.container	用于获取当前path下的所有兄弟节点(包括自身)。（其实就是数组，这个一会儿给大家演示）
path.type	获取当前path的节点类型。（等于 path.node.type 没啥说的）
path.key	获取当前path的key值。 或者说是获取当前node 的key值

path.get()  这个可以理解为取 path路径下的path。 什么意思呢？ 就是说，path路径下正常如果取它的节点应该是path.node.argument,但是这样就会得到一个 node，没有办法再继续用 path的那些方法了但是如果我们 path.get("argument") ,就可以得到 path.node.argument 的path这里面，除了传字符串之外，还可以传得更复杂，比如说path.get("argument.0")

path.getSibling(index)	获取当前路径对应节点的兄弟节点的路径。通过指定索引（index）可以获取相应的兄弟路径。
path.getFunctionParent()	获取当前路径对应节点的最近的函数父节点的路径。
path.getPrevSibling()	获取当前path的前一个兄弟节点，返回的是path类型。
path.getAllPrevSiblings()	获取当前path的所有前兄弟节点，返回的是Array类型，其元素都是path类型。
path.getNextSibling()	获取当前path的后一个兄弟节点，返回的是path类型。
path.getAllNextSiblings()	获取当前path的所有后兄弟节点，返回的是Array类型，其元素都是path类型。
path.evaluate()	用于计算表达式的值。
path.findParent()	向上查找满足回调函数特征的path，即判断上级路径是否包含有XXX类型的节点。
path.find()	功能与 path.findParent 方法一样，只不过从当前path开始进行遍历。
path.getFunctionParent()	获取函数类型父节点，如果不存在，返回 null。
path.getStatementParent()	获取Statement类型父节点，这个基本上都会有返回值，如果当前遍历的是 Program 或者 File 节点，则会报错。
path.getAncestry()	获取所有的祖先节点，没有实参，返回的是一个Array对象。
path.isAncestor(maybeDescendant)	判断当前遍历的节点是否为实参的祖先节点.
path.isDescendant(maybeAncestor)	判断当前遍历的节点是否为实参的子孙节点.
path.traverse(visitor)	遍历当前路径下的所有子节点，并应用指定的 visitor。
path.replaceWith(node)	用指定的节点替换当前路径对应的节点（单节点）。
path.replaceWithMultiple(node)	用指定的节点替换当前路径对应的节点（多节点，也就是 [] 类型）。
path.replaceWithSourceString(node) 替换资源字符串（这个不太常用）
path.replaceInline(node) 兼容了 replaceWithMultiple 与 replaceWith，如果不考虑性能无脑用它就可以（对性能影响其实可以忽略不计）
path.remove()	从 AST 中移除当前路径对应的节点。 // 个人的习惯和建议，删除放到最后在做
path.insertBefore(nodes) 在当前路径对应节点之前插入一个或多个节点。
path.insertAfter(nodes)	在当前路径对应节点之后插入一个或多个节点。
path.insertAfter(nodes)	在当前路径对应节点之后插入一个或多个节点。
path.toString()	用于将 AST 节点转换回对应的源代码字符串。

```



### 使用AST 流程

把混淆的js代码放到 https://astexplorer.net/ 中 观察结构

```js
// 导包
let parse = require("@babel/parser").parse
let generate = require("@babel/generator").default
let traverse = require("@babel/traverse").default
let types = require("@babel/types")
let fs = require('fs')

// input.js 为混淆的js代码  读取
let js_code = fs.readFileSync('input.js', 'utf-8')
// 将混淆的js代码 抽象为 抽象语法树
let ast = parse(js_code)

```

```js
let memory = {}
// 第一步 把常量 放到内存中 a b c e f
traverse(ast,{
    VariableDeclarator: function (path){
        let name = path.node.id.name;
        // 判断变量是否在节点中
        if(["a", "b", "e", "f"].indexOf(path.node.id.name) !== -1){
            // 判断变量值的类型是否是 ObjectExpression
            if(path.get('init').type === "ObjectExpression"){
                // 执行path 取到的代码
                eval(path.toString())
                // 把代码放到memory中
                memory[path.get("id").node.name] = path
            }
        }
    }
})
```

```js
// 第二步 还原 a对象中简单的字符串  type:  MemberExpression  这个类型对应  a['QxnwF']  直接把他的值替换过来即可
traverse(ast,{
    MemberExpression: function (path){
        // 判断前面的值是不是我有的  a b e f  且有值       StringLiteral 类型是 b['x']
        if(["a", "b", "e", "f"].indexOf(path.node.object.name) !== -1 && path.get('property').type === 'StringLiteral'){
            let result = eval(path.toString())
            // 如果 b['x'] 对应的值的类型是 string  直接替换
            if(typeof result === 'string'){
                // 用result 替换
                path.replaceInline({type:"StringLiteral", value: result})
            }
        }
    }
})
```

```js
// 第三步 控制流平坦化 拿到控制流的代码   SwitchCase 是 case '0'的类型
var b = "4|2|1|6|3|7|5|8|0"["split"]('|');
// 控制流的代码依次存入
var control = []
traverse(ast,{
    SwitchCase: function (path){
        // 将 case 0 : xx  中的 value 按照顺序 保存到control中  方便后续操作   consequent.0 是具体操作,  consequent.1 是continue
        control[path.get('test.value').node] = path.get('consequent.0').toString()
    }
})
// console.log(control)
```

```js
// 第三步2 控制流平坦化  替换while循环  按照 循环中的顺序 还原代码
traverse(ast,{
    WhileStatement: function (path){
        // 循环体 是 b[c++] -> b里的顺序  按照这个顺序把保存的control代码 还原
        let code = ''   // 正确顺序的代码
        for(let i of b){
            code += control[i]
        }// console.log(code)
        // 把code 替换为while循环
        path.replaceInline(parse(code))
    }
})
```

```js
// 第四步 还原a 中的函数
// 还原时分为两种情况 a['pAFiq'](e, 0x3e8) -> [g / h]  和  a["fpSNc"](g, h) -> [g(h)]
traverse(ast,{
    CallExpression: function (path){
        // 判断 call 方法执行的对象是不是 我已有的 对象  a b e f  先判断有没有 再判断是不是  不然会报错
        object_node = path.get('callee.object').node
        if(object_node && ["a", "b", "e", "f"].indexOf(object_node.name) !== -1){
            // console.log(path.toString())
            // 取之前保存对象的 memory[a] 的 每一行 properties i是 -> 'fpSNc': function (g, h) {return g(h);},
            for (let i of memory[object_node.name].get("init.properties")) {
                //          存在                                                memory中  QxnwF 对应的value是否等于 当前path对应的value
                if (path.get("callee").node && path.get("callee.property").node && i.node.key.value === path.get("callee.property").node.value) {
                    // console.log(path.toString())  得到了a中的所有执行的函数
                    // 接下来分为两种情况    操作符计算  BinaryExpression   函数执行  CallExpression
                    // console.log(i.get("value.body.body.0.argument").type)    就是 g(h) 的类型
                    if(i.get("value.body.body.0.argument").type === 'BinaryExpression'){  // 操作符计算
                        // 拿操作符
                        let operator = i.get("value.body.body.0.argument").node.operator
                        // 拿操作的 左节点
                        let left = path.get("arguments.0").node
                        // 右节点
                        let right = path.get("arguments.1").node
                        // console.log(left ,operator, right)
                        // 然后把整个path节点还原
                        path.replaceInline(types.binaryExpression(operator, left, right))
                    }
                    else if(i.get("value.body.body.0.argument").type === 'CallExpression'){ // 函数执行
                        // console.log(path.toString())
                        // 拿 左节点
                        let function_path = path.get("arguments.0").node
                        // 拿 其他的节点   函数执行是 第一个参数执行(后面所有参数)
                        let function_arguments = path.node.arguments.splice(1)
                        // 把整个path得到的节点还原
                        path.replaceInline(types.callExpression(function_path, function_arguments))
                    }
                }
            }
        }
    }
})
```

```js
// 第五步 删除无效代码 a b e f 删除最好放在后面 防止出现问题
traverse(ast,{
    VariableDeclarator: function (path){
        let name = path.node.id.name;
        // 判断变量是否在节点中
        if(["a", "b", "e", "f"].indexOf(path.node.id.name) !== -1){
            // console.log(path.toString())
            path.remove()
        }
    }
})
```

```js
// 接下来 标准化还原的结果
// 01.将所有字符串字面量 统一按照raw 格式输出
traverse(ast, {
    StringLiteral: function (path){
        if(path.node.extra){
            path.node.extra.raw = "'" + path.node.value + "'"
            // console.log(path.toString())
        }
    }
})
```

```js
/*
02.把可读性差的b['x'] 转化成 b.x
原b['x']的 ast树
MemberExpression {
    object: Identifier("b")
    computed: true
    property: StringLiteral("IzFOn")
}
拼凑b.x的 ast树
MemberExpression {
    object: Identifier("b")
    computed: false
    property: Identifier("IzFOn")
}
*/
traverse(ast, {
    MemberExpression: function (path){
        path.node.computed = false
        path.node.property.type = "Identifier"
        path.node.property.name = path.node.property.value
    }
})
```

```js
// 03.把（"a" + "b"）计算成 "ab" 并替换回 AST 中
traverse(ast, {
    BinaryExpression: function (path){
        let left = path.get("left").node.value
        let right = path.get("right").node.value
        if(path.get("left").isStringLiteral() && path.get("right").isStringLiteral()){
            path.replaceInline(types.valueToNode(left + right))
        }
    }
})
```

```js
// 04.删掉 用不上的 $_oc
traverse(ast, {
    FunctionDeclaration: function(path){
        if(path.node.id.name === "_$oc"){
            path.remove()
        }
    }
})
```

### 常用AST类型列表

| 代码形式             | property 类型         | computed | 示例说明                      |
| -------------------- | --------------------- | -------- | ----------------------------- |
| **b['x']**           | StringLiteral         | true     | 字符串 key                    |
| **b["hello"]**       | StringLiteral         | true     | 双引号字符串                  |
| **b['123']**         | StringLiteral         | true     | 字符串数字                    |
| **b[0]**             | NumericLiteral        | true     | 数组索引                      |
| **b[1.23]**          | NumericLiteral        | true     | 浮点数索引                    |
| **b[x]**             | Identifier            | true     | 变量作为 key                  |
| **b[_0x12abc]**      | Identifier            | true     | 混淆变量名作为 key            |
| **b[x + y]**         | BinaryExpression      | true     | 表达式作为 key                |
| **b[i++]**           | UpdateExpression      | true     | 自增表达式 key                |
| **b[func()]**        | CallExpression        | true     | 函数返回值作为 key            |
| **b[a ? 'x' : 'y']** | ConditionalExpression | true     | 三元表达式作为 key            |
| **b[`x`]**           | TemplateLiteral       | true     | 模板字符串 key                |
| **b[`${x}y`]**       | TemplateLiteral       | true     | 动态模板字符串 key            |
| **b[/abc/]**         | RegExpLiteral         | true     | 正则表达式 key（极罕见）      |
| **b[{a:1}]**         | ObjectExpression      | true     | 对象字面量作为 key（无效 JS） |
| **b[Symbol()]**      | CallExpression        | true     | symbol 作为 key               |
| **b.x**              | Identifier            | false    | 非计算属性（点操作符）        |
| **b._0xabc123**      | Identifier            | false    | 混淆变量名                    |
| **b.true**           | Identifier            | false    | 保留字作为 key（可编译）      |
| **b["x"].y**         | Identifier            | false    | 连续属性访问                  |
| **b?.x**             | Identifier            | false    | 可选链访问（OptionalMember）  |
