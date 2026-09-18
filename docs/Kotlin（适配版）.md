---
title: "Kotlin"
date: 2026-09-16
post_status: publish
comment_status: open
taxonomy:
  category:
    - 计算机
  post_tag:
    - Kotlin

---

# Kotlin 基础完整学习笔记 + 可运行案例

建议：新建 Kotlin/JVM Library 模块运行下面所有代码，不要放在 Android app 模块，避免SourceSet报错。
## 1. 变量声明 val /var
* val：**只读（final）**，赋值后不能修改，优先使用 val
* var：**可变**，可以重新赋值
* Kotlin **类型自动推导**，很多时候不用写:类型
```
fun main() {
    // val 只读，不可修改
    val name: String = "张三"
    // name = "李四" //编译报错！val不能二次赋值

    // var 可变变量
    var age: Int = 18
    age = 22

    // 类型自动推导，编译器自动识别类型，可以省略类型
    val height = 175.3 // Double
    val isStudent = true // Boolean

    println(name)
    println(age)
    println(height)
}
```
## 2. 基础数据类型
表格

| 类型      | 说明    | 示例                   |
| ------- | ----- | -------------------- |
| Int     | 整数    | val a:Int = 10       |
| Double  | 小数双精度 | val d = 3.14         |
| Float   | 单精度小数 | val f = 3.14f        |
| Long    | 长整型   | val l = 1000L        |
| Boolean | 布尔    | val b = true / false |
| Char    | 单个字符  | val c = 'A'          |
| String  | 字符串   | val str = "hello"    |

Kotlin 没有基础原始类型，全部都是对象。
## 3. 字符串模板 $
$变量名 直接嵌入字符串；复杂表达式 ${表达式}
```
fun main() {
    val name = "小明"
    val age = 20
    // 简单变量 $
    val info1 = "姓名：$name，年龄：$age"
    // 表达式 ${ }
    val info2 = "明年年龄：${age + 1}"

    println(info1) //姓名：小明，年龄：20
    println(info2) //明年年龄：21

    // 多行字符串 """
    val multiStr = """
        第一行文本
        第二行文本
        姓名=$name
    """.trimIndent()
    println(multiStr)
}
```
## 4. 可空类型 ? 、安全调用 ?. 、Elvis 运算符 ?: 
Kotlin 默认变量不能为 null，想要存 null 必须加?声明可空类型
* 变量?：标记这个变量允许为 null
* ?.：安全调用，变量为 null 的时候，直接返回 null，不会空指针崩溃
* ?: Elvis，如果左边结果是 null，返回右边默认值
* !!：强制非空，告诉编译器一定不为 null，为 null 会直接崩溃，开发尽量少用
```
fun main() {
    // 普通String，不能赋值null
    // var str:String = null //编译报错

    // ? 可空类型，可以存null
    var phone: String? = null

    phone = "13912345678"

    //安全调用 ?.length ，如果phone=null不会报错
    println(phone?.length)

    // Elvis ?: null的时候返回默认值0
    val len = phone?.length ?: 0
    println(len)

    phone = null
    val len2 = phone?.length ?: -1
    println(len2) //-1

    // !! 强制非空，phone=null会直接抛出空指针异常，慎用
    // println(phone!!.length)
}
```
## 5. 条件判断 if-else
Kotlin 中 if 是表达式，可以有返回值，不需要三元运算符
```
fun main() {
    val score = 75
    // 普通if else
    if (score >= 60) {
        println("及格")
    } else {
        println("不及格")
    }

    // if作为表达式，返回结果赋值给变量
    val result = if (score >=60) "及格" else "不及格"
    println(result)
}
```
## 6. when 多分支（替代 Java switch）
支持常量、区间、条件判断，强大很多
```
fun main() {
    val num = 3
    when(num){
        1 -> println("数字1")
        2 -> println("数字2")
        3 -> println("数字3")
        else -> println("其他数字")
    }

    // when表达式，返回值
    val msg = when(num){
        1 -> "一"
        2 -> "二"
        in 3..10 -> "3到10之间" //区间判断
        else -> "未知"
    }
    println(msg)
}
```
## 7. 循环 for /while
for 循环
```
fun main() {
    // 区间 1..10  [1,10] 包含10
    for(i in 1..10){
        print("$i ")
    }
    println()

    // until：不包含结束值 1 until 10 →19
    for(i in 1 until 10){
        print("$i ")
    }
    println()

    // step 步长
    for(i in 1..10 step 2){
        print("$i ")
    }
    println()

    // downTo 倒序
    for(i in 10 downTo 1){
        print("$i ")
    }
    println()

    //遍历集合
    val list = listOf("苹果","香蕉","橙子")
    for(item in list){
        println(item)
    }
}
```
while / do while
```
fun main() {
    var i = 0
    while(i < 5){
        println(i)
        i++
    }

    // do while 至少执行一次
    var j =0
    do {
        println(j)
        j++
    }while(j<3)
}
```
## 8. 函数 fun
语法：fun 函数名(参数:类型):返回值类型 { }
* 返回值 Unit等价 Java void，可以省略不写
```
//无返回值
fun sayHello(name: String){
    println("Hello $name")
}

//有返回值 Int
fun add(a:Int, b:Int): Int{
    return a + b
}

//单表达式函数，可以简化写法，省略return
fun addShort(a:Int,b:Int) = a + b

//参数默认值
fun showInfo(name:String, age:Int = 18){
    println("姓名:$name 年龄:$age")
}

fun main() {
    sayHello("Kotlin")
    println(add(3,5))
    println(addShort(2,4))
    showInfo("张三") // age使用默认值18
    showInfo("李四", 25)
}
```
## 9. 类与对象 class

```
//普通类
class Person {
    var name: String = ""
    var age: Int = 0

    fun show(){
        println("name=$name age=$age")
    }
}

//主构造函数简写（最常用）
class Student(val name: String, var age: Int) {
    fun printInfo(){
        println("学生：$ name，$age岁")
    }
}

fun main() {
    val p = Person()
    p.name = "老王"
    p.age = 30
    p.show()

    val s = Student("小张",16)
    s.printInfo()
    // s.name = "aaa" // val只读，不能修改
    s.age =17 // var可以修改
}
```

## 伴生对象 companion object
相当于 Java 静态成员，Kotlin 没有 static 关键字
```
class Demo{
    companion object{
        val VERSION = "1.0"
        fun staticFunc(){
            println("伴生对象函数，类似静态方法")
        }
    }
}

fun main() {
    println(Demo.VERSION)
    Demo.staticFunc()
}
```
## 10. 集合 List / MutableList；Set / Map
* 只读集合：listOf()，不能增删改
* 可变集合：mutableListOf()，可以 add remove
```
fun main() {
    //只读List
    val list = listOf("A","B","C")
    println(list[0])

    //可变List
    val mList = mutableListOf<String>()
    mList.add("张三")
    mList.add("李四")
    mList.remove("张三")
    println(mList)

    // Map 键值对
    val map = mapOf("a" to 1, "b" to 2)
    println(map["a"])

    val mMap = mutableMapOf<String,Int>()
    mMap["key1"] = 100
    println(mMap["key1"])
}
```
## 11. 空安全综合完整案例（你截图那套代码完整版）
```
fun main() {
    // val只读
    val name: String = "张三"

    // var可变
    var age: Int =18
    age =20

    //自动推导类型
    val height =175.5

    //字符串模板
    val info = "姓名：$name，年龄：$age，身高：${height}cm"
    println(info)

    //可空类型
    var phone: String? = null
    phone = "13800138000"

    //安全调用 ?.
    println(phone?.length)

    //Elvis ?:
    val len = phone?.length ?: 0
    println(len)
}
```
# Kotlin 学习顺序建议
1.val/var、基础数据类型
2.字符串模板
3.可空类型？?. ?:（Kotlin 最重要特性，区分 Java）
4.if-else、when、循环
5.函数 fun、默认参数
6.类、构造函数、伴生对象
7.集合 List/Map
8.继承、接口、数据类 data class
9.Lambda、高阶函数
10.协程（Android 开发重点）
Text(
    text = "张三今年18岁",
    color = Color.Red,                 //文字颜色
    fontSize = 20.sp,                  //字号 sp
    fontWeight = FontWeight.Bold,      //字重（粗体）
    fontStyle = FontStyle.Italic,      //斜体
    letterSpacing = 2.sp,              //字间距
    lineHeight = 30.sp,                //行高
    maxLines = 2,                      //最大显示行数
    overflow = TextOverflow.Ellipsis,  //文字溢出：...省略号
    textAlign = TextAlign.Center,      //文字对齐
    textDecoration = TextDecoration.Underline, //下划线
    modifier = Modifier
        .background(Color.LightGray)   //文字背景底色
        .padding(10.dp)                //内边距
)
# 逐个解释
## 1. 字体粗细 fontWeight
fontWeight = FontWeight.Bold     //粗体
fontWeight = FontWeight.Normal   //正常（默认）
fontWeight = FontWeight.Light    //细体
## 2. 斜体 fontStyle
fontStyle = FontStyle.Italic   //斜体
fontStyle = FontStyle.Normal   //正常
## 3. 字间距 letterSpacing 字符之间拉开距离
letterSpacing = 1.sp
## 4. 行高 lineHeight，多行文字每行之间距离
lineHeight = 28.sp
## 5. 行数控制、文字溢出（长文本）
maxLines = 1,                          //只允许1行
overflow = TextOverflow.Ellipsis,       //超出显示 …
// overflow = TextOverflow.Clip        //直接截断切掉
// overflow = TextOverflow.Visible    //全部显示，溢出
## 6. 文字对齐 textAlign
textAlign = TextAlign.Center     //居中
textAlign = TextAlign.Start      //靠左(默认)
textAlign = TextAlign.End        //靠右
textAlign = TextAlign.Justify    //两端对齐
⚠️注意：textAlign生效需要 Text 本身有足够宽度，Modifier.fillMaxWidth ()
Text(
    "张三今年18岁",
    textAlign = TextAlign.Center,
    modifier = Modifier.fillMaxWidth()
)
## 7. 下划线、删除线 textDecoration
textDecoration = TextDecoration.Underline      //下划线
textDecoration = TextDecoration.LineThrough   //删除线（划掉文字）
textDecoration = TextDecoration.None          //无装饰默认
8.modifier 给 Text 组件加修饰（背景、边距）
modifier = Modifier
    .background(Color(0xFFEEEEEE)) //背景颜色
    .padding(horizontal = 15.dp, vertical = 8.dp)
    .fillMaxWidth()
## 8. 使用现成 Material3 文字样式（推荐正式项目）
不用自己写一堆 fontSize、fontWeight，直接套主题样式
Text(
    "张三今年18岁",
    style = MaterialTheme.typography.titleMedium
)
1️⃣ 显示文字：Text
var age = 20
Text("小李今年$age 岁", fontSize = 20.sp, color = Color.Black)
2️⃣ 输入框：OutlinedTextField（你写奇偶判断用过）
用户输入文字
var inputText by remember { mutableStateOf("") }
OutlinedTextField(
    value = inputText,
    onValueChange = { inputText = it },
    label = { Text("请输入名字") }
)
3️⃣ 按钮：Button / ElevatedButton
点击触发事件
var count by remember { mutableStateOf(0) }
Button(onClick = { count++ }) {
    Text("点击：$count")
}

// 凸起按钮
ElevatedButton(onClick = {}) {
    Text("凸起按钮")
}

//文字按钮，无背景
TextButton(onClick = {}) {
    Text("文字按钮")
}
4️⃣ 布局容器（放别的控件）
Column：垂直排列（从上往下）
Column {
    Text("第一行")
    Text("第二行")
}
Row：水平排列（从左往右）
Row {
    Text("左边")
    Text("右边")
}
Box：层叠布局，控件可以重叠
Box {
    Text("底层文字")
    Text("盖在上面", color = Color.Red)
}
5️⃣ 复选框 Checkbox
勾选、取消勾选
var checked by remember { mutableStateOf(false) }
Checkbox(
    checked = checked,
    onCheckedChange = { checked = it }
)
Text(text = if(checked) "已勾选" else "未勾选")
6️⃣ 单选按钮 RadioButton
多选一
var selectId by remember { mutableStateOf(1) }
Row {
    RadioButton(
        selected = selectId ==1,
        onClick = { selectId =1 }
    )
    Text("选项A")

    RadioButton(
        selected = selectId ==2,
        onClick = { selectId =2 }
    )
    Text("选项B")
}
7️⃣ 开关 Switch
类似手机设置开关
var switchState by remember { mutableStateOf(false) }
Switch(
    checked = switchState,
    onCheckedChange = { switchState = it }
)
8️⃣ 滑块 Slider
拖动选择数字
var progress by remember { mutableStateOf(50f) }
Slider(
    value = progress,
    onValueChange = { progress = it },
    valueRange = 0f..100f
)
Text("当前数值：${progress.toInt()}")
9️⃣ 图片 Image
显示图片资源
Image(
    painter = painterResource(id = R.mipmap.ic_launcher),
    contentDescription = "图标",
    modifier = Modifier.size(60.dp)
)
🔟 分割线 Divider
画一条横线做分隔
Divider(thickness = 1.dp, color = Color.Gray)
11️⃣ 列表 LazyColumn（最重要！长列表，替代 ListView）
滚动列表，类似 RecyclerView
val list = remember { mutableStateListOf("苹果","香蕉","橙子") }
LazyColumn {
    items(list) { item ->
        Text(item, modifier = Modifier.padding(10.dp))
    }
}
12️⃣ 下拉菜单 DropdownMenu
下拉选择框
var expand by remember { mutableStateOf(false) }
var selectText by remember { mutableStateOf("请选择") }

Button(onClick = { expand = true }) {
    Text(selectText)
}
DropdownMenu(expanded = expand, onDismissRequest = { expand=false }) {
    DropdownMenuItem(text={Text("北京")}, onClick = { selectText="北京"; expand=false })
    DropdownMenuItem(text={Text("上海")}, onClick = { selectText="上海"; expand=false })
}
13️⃣ Card 卡片
带圆角阴影卡片容器
Card(modifier = Modifier.padding(10.dp)) {
    Text("卡片里面的文字", modifier=Modifier.padding(16.dp))
}



快速记忆分类
1.显示类：Text、Image
2.输入交互：OutlinedTextField、Checkbox、RadioButton、Switch、Slider
3.点击：Button、ElevatedButton、TextButton
4.布局容器：Column(垂直)、Row(水平)、Box(层叠)、Card
5.滚动列表：LazyColumn（垂直列表） / LazyRow（水平列表）
6.辅助：Divider分割线

