---
title: "第 4 课 Lombok + 开发环境搭建"
date: 2026-08-11
post_status: publish
comment_status: open
taxonomy:
  category:
    - 项目
  post_tag:
    - 项目搭建学习
---

# 第 4 课 Lombok + 开发环境搭建

> 本课两部分：① 认识 Lombok——一个帮你少写「样板代码」的利器，学完能看懂项目里 85 个文件都在用的注解；② 把开发环境（JDK 21 + IDEA + Lombok 插件 + Maven）搭好、能自检。学完你就可以真正「动手跑项目」了。

---

## 本课学习目标

完成本课后，你将能够：

1. 理解 Lombok 的原理（编译期自动生成代码）
2. 认识项目常用的 6 个 Lombok 注解，并在源码中找到真实用例
3. 分清「哪些类用 Lombok、哪些不用」——并纠正一个常见文档错误
4. 搭好并自检开发环境：JDK 21 / IDEA / Lombok 插件 / Maven
5. 了解 Git 基础工作流

---

## 一、知识点详解

### 1.1 Lombok 是什么

Java 的「样板代码」很啰嗦：一个实体类要写一堆 getter/setter、toString、构造器。**Lombok** 是编译期注解处理器——你在类上写 `@Data`，编译时它**自动帮你生成**这些方法，源码里干净，`.class` 里方法齐全。

- 依赖已由根 `pom.xml` 的 `<dependencies>` 统一声明（版本由 spring-boot-starter-parent 管理），所有模块都能用。
- **IDEA 必须装 Lombok 插件**，否则编译报「cannot find symbol 方法 getXxx()」——因为 IDEA 默认不认识这些自动生成的方法。

### 1.2 项目常用的 6 个注解（真实用例）

全项目共 **133 处 / 85 个文件**用到 Lombok，常用的是下面 6 个。

#### ① `@Data` —— 一键生成 Getter/Setter/ToString/equals/hashCode
**真实用例** —— `novel-front/.../vo/BookVO.java`（第 13-14 行）：

```java
@Data
public class BookVO extends Book implements Serializable {
    @JsonFormat(timezone = "GMT+8", pattern = "MM/dd HH:mm")
    private Date lastIndexUpdateTime;
}
```

`BookVO` 继承了实体 `Book`，自己只加了一个字段。没有 Lombok 的话，它要复制 `Book` 的一大堆 getter/setter，这里一行 `@Data` 全搞定。

#### ② `@Slf4j` —— 直接获得日志对象 `log`
**真实用例** —— `novel-front/.../FrontNovelApplication.java`（第 28-29 行）：

```java
@Slf4j
public class FrontNovelApplication {
    // 编译后自动生成 private static final Logger log = ...;
    public static void main(String[] args) {
        SpringApplication.run(FrontNovelApplication.class);
        log.info("项目启动啦...");   // 直接用 log，不用手动 new Logger
    }
}
```

#### ③ `@RequiredArgsConstructor` —— 为 final 字段生成构造器（配合构造器注入）
**真实用例** —— `novel-front/.../service/impl/LikeServiceImpl.java`（第 19-23 行）：

```java
@Service
@RequiredArgsConstructor
public class LikeServiceImpl implements LikeService {
    private final StringRedisTemplate redisTemplate;   // final 字段
    ...
}
```

它会给**所有 `final` 字段**生成一个构造器，Spring 用这个构造器做**依赖注入**（比 `@Autowired` 字段注入更推荐）。这是后面学「请求链路怎么组装」的地基。

#### ④ `@SneakyThrows` —— 把受检异常「偷偷」变成非受检
**真实用例** —— `novel-front/.../controller/PayController.java`（第 47 行）、`JwtTokenUtil.java`（第 107 行）：

```java
@SneakyThrows
public void alipayCallback(HttpServletRequest request) {
    ... // 里面直接调用会抛 Exception 的方法，不用写 try-catch
}
```

#### ⑤ `@Getter` + `@AllArgsConstructor` + `@NoArgsConstructor` —— 按需组合
**真实用例** —— `novel-common/.../core/enums/ResponseStatus.java`（第 12-14 行，枚举类）：

```java
@Getter
@AllArgsConstructor
@NoArgsConstructor
public enum ResponseStatus {
    OK(0, "成功"),
    FAIL(1, "失败");
    ...
}
```

给枚举生成 `getValue()/getMsg()` 和带参/无参构造器，配合枚举常量使用。

#### ⑥ `@EqualsAndHashCode(callSuper = true)` —— 继承场景下重写 equals/hashCode
**真实用例** —— `novel-crawl/.../vo/CrawlSourceVO.java`（第 13 行）：

```java
@Data
@EqualsAndHashCode(callSuper = true)   // 把父类字段也算进 equals/hashCode
public class CrawlSourceVO extends CrawlSource {
```

**没用到**：`@Builder`、`@Accessors` 等（项目风格未用，但你写新代码时 `@Builder` 很好用）。

### 1.3 重点认知：哪些类用 Lombok，哪些不用

**一个容易踩的认知坑**：`doc/tech-stack-learning-roadmap.md` 2.3 节说「所有 entity 类都用了 @Data」——**但实际不是**。

打开 `novel-common/.../entity/Book.java` 看看真相：

```java
public class Book implements Serializable {
    @Generated("org.mybatis.generator.api.MyBatisGenerator")
    private Long id;
    ...
    @Generated("org.mybatis.generator.api.MyBatisGenerator")
    public Long getId() { return id; }        // 完整的 getter/setter 都手写着
    public void setId(Long id) { this.id = id; }
    ...
}
```

**`Book` 等 24 个实体类，一个 Lombok 注解都没有**——它们是 **MyBatis Generator 代码生成器**生成的纯 POJO（用 `@Generated("...MyBatisGenerator")` 标注来源），生成器已经把所有 getter/setter 写全了，不需要 Lombok。

规律总结：

| 类 | 用 Lombok？ | 为什么 |
|---|---|---|
| 生成的实体 `entity/*.java`（Book 等） | ❌ 不用 | 生成器已生成全部 getter/setter |
| 手写的 VO / Controller / Service / Config / 枚举 / 工具类 | ✅ 用 | 手写时用 Lombok 省样板代码 |

再看 `BookVO extends Book` 的例子：父类 `Book` 没注解，子类 `BookVO` 手写所以用 `@Data`——**「用不用 Lombok」取决于「代码是不是手写的」，不是「是不是 entity」**。

### 1.4 开发环境搭建（照做一遍）

**① JDK 21**
- 去 Oracle 或 OpenJDK 下载 JDK 21 安装包，配置环境变量 `JAVA_HOME`，把 `%JAVA_HOME%\bin` 加入 `Path`。
- 验证：命令行执行 `java -version`，看到 `version "21"` 即成功。

**② IDEA + Lombok 插件**
- 安装 IntelliJ IDEA（Community 免费版即可）。
- **必须装插件**：`File → Settings → Plugins → Marketplace` 搜索 **Lombok** 安装。不装会报编译错误。
- 若用新版 IDEA，可能已内置 Lombok 支持，但建议确认。

**③ Maven**
- 用 IDEA 自带 Maven，或独立安装 Maven 3.9+。
- 建议配 `settings.xml` 的阿里镜像加速（`maven.aliyun.com`），并注意第 3 课讲的 `mirrorOf=*` 会拦截 `xxyopen` 仓库的坑。

**④ 导入项目**
- IDEA 里 `Open` → 选择根目录的 **`pom.xml`** → 以 Maven 工程打开。四个模块会被正确识别为多模块工程。
- 首次会下载依赖，等右下角进度条完成。

**⑤ MySQL / Redis**
- 见第 1 课：装好 MySQL 8.x 与 Redis，用 `doc/sql/novel_plus.sql` 初始化数据库。

### 1.5 Git 基础工作流（了解）

- Git 用于版本管理：`git clone <地址>` 拿到代码 → 建分支 `git checkout -b feature/xxx` 开发 → `git add` + `git commit` 提交 → `git push` + 发起 **Pull Request** 合入主干。
- `.gitignore` 用来排除不该提交的文件（如 `target/`、`.idea/`）。
- **注意**：你当前这个本地目录**还不是 git 仓库**（没有 `.git`），如果要做自己的版本管理，可在项目根执行 `git init` 再提交（自行斟酌，别把含 api-key 的配置文件传上公开仓库）。

---

## 二、动手练习（含验证标准）

> 做完一项勾一项。

### 练习 1：环境自检
- **目标**：确认 JDK 21 / Maven / Lombok 插件就绪。
- **步骤**：命令行跑 `java -version`、`mvn -version`；IDEA 里 `Settings → Plugins` 确认 Lombok 已安装。
- **验证标准**：`java` 输出 `version "21"`；`mvn` 能输出版本；IDEA 插件列表能看到 Lombok。

### 练习 2：对比两类类
- **目标**：直观感受「纯 POJO vs @Data」的代码量差异。
- **步骤**：用 Ctrl+Shift+N 打开 `Book.java`（entity）和 `BookVO.java`（vo），比较行数与 getter/setter 写法。
- **验证标准**：能说出——Book 是生成器写全 getter/setter 的纯 POJO；BookVO 只写字段 + 一个 `@Data`。

### 练习 3：体验 Lombok 自动生成
- **目标**：亲眼看到 `@Data` 生成了什么。
- **步骤**：在 IDEA 的 Scratch File 里写一个 `@Data class Student { private String name; }`，然后按 Ctrl+F12 看类结构。
- **验证标准**：能看到 `getName()/setName()/toString()/equals()/hashCode()` 等自动生成的方法。

### 练习 4（选做）：验证插件生效
- **目标**：确认不因缺插件报错。
- **步骤**：在根目录执行 `mvn compile`（或 IDEA 里 Build），观察是否报「cannot find symbol ... getXxx」。
- **验证标准**：`BUILD SUCCESS`，无找不到方法错误。

---

## 三、本课小结

Lombok 是编译期生成样板代码的工具，项目里 85 个文件用到它——最常用 `@Data`、`@Slf4j`、`@RequiredArgsConstructor`、`@SneakyThrows`，枚举和继承场景还会用到 `@Getter/@AllArgsConstructor/@NoArgsConstructor`、`@EqualsAndHashCode(callSuper=true)`。**但要注意**：MyBatis Generator 生成的实体类是纯 POJO，不用 Lombok；Lombok 只服务于手写类（VO/Controller/Service/Config/工具/枚举）。环境上，JDK 21 + IDEA + **Lombok 插件** + Maven 齐了就具备了「动手跑项目」的条件。

---

## 四、自测题

1. 【选择】`@Data` 会自动生成哪些内容？（A. getter/setter　B. toString　C. equals/hashCode　D. 以上都是）
2. 【选择】`@RequiredArgsConstructor` 会给哪些字段生成构造器？（A. static 字段　B. final 字段　C. transient 字段　D. 所有字段）
3. 【选择】下列哪个注解可以把受检异常「偷偷」变成非受检、免写 try-catch？（A. `@Slf4j`　B. `@Data`　C. `@SneakyThrows`　D. `@Getter`）
4. 【简答】为什么 MyBatis Generator 生成的 `Book.java` 不需要 Lombok？
5. 【简答】`@Slf4j` 在类里提供了哪个变量名可以直接用？

> 答案：1-D、2-B、3-C（见 1.2）、4-生成器已生成完整 getter/setter（见 1.3）、5-`log`（见 1.2②）。

---

## 五、参考资源

- 本课程大纲：`Tutorial/课程大纲-30节课.md` → 第 4 课
- 技术栈路线：`doc/tech-stack-learning-roadmap.md` → 2.3 节 Lombok（注意其「所有 entity 用 @Data」的说法与源码不符）
- 官方文档：projectlombok.org/features
- 环境下载：Oracle JDK 21 下载页、IntelliJ IDEA 官网
