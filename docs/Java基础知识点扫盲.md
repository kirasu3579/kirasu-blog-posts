---
title: "Java基础知识点扫盲"
date: 2026-07-04
post_status: publish
comment_status: open
taxonomy:
  category:
    - Java
  post_tag:
    - Java
---
<iframe width="560" height="315" src="https://player.bilibili.com/player.html?bvid=BV1Jp4y1t7yG&amp;page=1&amp;high_quality=1&amp;danmaku=0" title="Bilibili video player" frameborder="0" allowfullscreen=""></iframe>



---

## 01-面向对象

### 一、面向对象 vs 面向过程

1. 面向过程将任务拆解成一系列步骤，每个步骤对应一个函数，按顺序执行。
2. 面向对象则先分析需求中有哪些参与者（对象），再明确每个对象各自需要做什么。
3. 面向过程更注重事情的步骤和顺序，面向对象更注重需求中的对象及其职责划分。
4. 面向过程直接高效，想到什么就做什么；面向对象需要先分析再设计，有一个分析过程。
5. 面向对象更易于复用、扩展和维护，而面向过程在性能方面更有优势。

### 二、封装

6. 封装的意义在于明确标识出允许外部使用的成员，内部细节对外部调用者透明。
7. 封装让外部调用者只需知道方法怎么调用，无需关心内部具体实现。
8. Java 中封装的经典场景之一：JavaBean 将属性私有化，通过 get/set 方法对外提供访问入口。
9. JavaBean 封装可保证属性的赋值和获取逻辑（如命名规则）由类本身控制，防止外部随意修改。
10. 封装的经典场景之二：使用 ORM 框架（如 MyBatis）时，无需关心连接建立、SQL 执行等细节，直接调用方法即可，框架封装了底层操作。

### 三、继承

11. 继承是指子类通过 extends 关键字继承父类，复用父类的方法并可以做出自己的改变或扩展。
12. 继承将多个子类的共性内容抽取到父类中，子类只需关注自己个性化的部分，达到代码复用、减少冗余的目的。

### 四、多态

13. 多态的三个条件：存在继承关系、子类重写父类方法、父类引用指向子类对象。
14. 多态的含义：基于对象所属类的不同，外部对同一个方法的调用，实际执行的逻辑不同。
15. 多态的好处：更换子类实现时，只需修改 new 的对象，调用方的代码无需改动，利于程序维护和扩展。
16. 多态的弊端：无法调用子类特有的、非重写父类的方法，因为调用的方法必须在父类中有定义。

### 五、面试回答要点

17. 回答“什么是面向对象”时，既要讲清面向对象与面向过程的区别，也要涵盖封装、继承、多态三大特性，否则只算答对了一小半。



<iframe width="560" height="315" src="https://player.bilibili.com/player.html?bvid=BV1Jp4y1t7yG&amp;page=2&amp;high_quality=1&amp;danmaku=0" title="Bilibili video player" frameborder="0" allowfullscreen=""></iframe>

## 02-JDK、JRE、JVM区别和联系

---

1. JDK 全称是 Java Development Kit（Java 开发工具包），是提供给开发人员使用的。
2. JRE 全称是 Java Runtime Environment（Java 运行时环境），是提供给仅需运行 Java 程序的普通用户使用的。
3. JVM 是 Java 虚拟机，用于将 .class 文件解释成机器码，供操作系统执行。
4. JDK 安装包中实际上已经包含了完整的 JRE。
5. JRE 的核心包含两个目录：bin 目录（即 JVM）和 lib 目录（存放 Java 核心类库，如 rt.jar）。
6. JDK = JRE + 开发工具（如 javac、java、jconsole、jdb 等）。
7. 三者的包含关系为：JDK 包含 JRE，JRE 包含 JVM。
8. Java 源文件（.java）先由 javac 编译成 .class 字节码文件，再由 JVM 解释执行。
9. JVM 拥有 Windows、Linux 等多个操作系统版本，这是 Java 实现"一次编译，到处运行"的根本原因。
10. "一次编译，到处运行"指的是同一份 .class 文件可以在不同操作系统的 JVM 上运行，而不是 JVM 本身可以到处运行。
11. JVM 在解释 .class 文件时，会借助 lib 目录中的核心类库将字节码翻译成机器码，再映射并调用操作系统接口，最终让程序运行起来