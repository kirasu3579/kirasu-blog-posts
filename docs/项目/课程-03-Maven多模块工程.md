---
title: "第 3 课 Maven 多模块工程"
date: 2026-08-11
post_status: publish
comment_status: open
taxonomy:
  category:
    - 项目
  post_tag:
    - 项目搭建学习
---

# 第 3 课 Maven 多模块工程

> 本课讲清这个项目的「工程骨架」：它不是一个 Spring Boot 单项目，而是一个 Maven 多模块工程。学完你能读懂任何 pom.xml——包括本项目中一个很有意思的「例外模块」。

---

## 本课学习目标

完成本课后，你将能够：

1. 理解 Maven 坐标三要素与多模块聚合的关系
2. 看懂根 pom 的 `modules` / `parent` / `dependencyManagement` 在干什么
3. 理解「版本统一三板斧」：properties 占位符、BOM、继承 starter-parent
4. 认识 **novel-admin 例外模块**（Spring Boot 2.7.18、不依赖 common）并解释其影响
5. 会用 `mvn` 常用命令构建，知道 mirrorOf 拦截坑

---

## 一、知识点详解

### 1.1 Maven 与坐标

Maven 是 Java 项目的**构建 + 依赖管理工具**：它负责「依赖包从哪下载、按什么顺序编译打包、产物是什么」。每个 Maven 项目都有一个 `pom.xml`（Project Object Model），项目之间靠**坐标**唯一标识：

```xml
<groupId>com.java2nb</groupId>        <!-- 组织/公司域名反写 -->
<artifactId>novel-front</artifactId>  <!-- 模块名 -->
<version>5.3.3</version>              <!-- 版本号 -->
```

有了坐标，模块之间就可以互相引用、从远程仓库下载第三方库。

### 1.2 多模块骨架：一个父工程 + 四个子模块

整个项目是一个**聚合工程**。根目录 `pom.xml` 只负责「把四个模块组织起来」：

```xml
<!-- 根 pom.xml 关键片段 -->
<packaging>pom</packaging>            <!-- 父工程不打 jar，只做聚合 -->

<modules>                             <!-- 聚合：声明有哪些子模块 -->
    <module>novel-common</module>
    <module>novel-front</module>
    <module>novel-crawl</module>
    <module>novel-admin</module>
</modules>
```

子模块（以 `novel-front/pom.xml` 为例）则通过 `<parent>` 声明「我是谁的子模块」：

```xml
<parent>
    <artifactId>novel</artifactId>
    <groupId>com.java2nb</groupId>
    <version>5.3.3</version>
</parent>
```

完整依赖关系（一图流）：

```
pom.xml（根，packaging=pom）            ← Spring Boot 3.4.0
 ├── novel-common（jar，公共库：Web/MyBatis/Redis/Sharding/工具）
 ├── novel-front（jar，可运行）──依赖──▶ novel-common
 ├── novel-crawl（jar，可运行）──依赖──▶ novel-common
 └── novel-admin（jar，可运行，特例！见 1.5）
```

> 记忆点：**common 是被别人依赖的「地基」；front 看书、crawl 爬书、admin 管书**。`mvn package` 会按依赖顺序自动构建 common → front/crawl → admin。

### 1.3 版本统一三板斧

多模块最怕「每个模块各写各的版本号，升级时改疯」。本项目用三招解决：

**① properties 占位符** —— 根 pom 里把版本集中声明为属性，子模块用 `${...}` 引用：

```xml
<properties>
    <java.version>21</java.version>
    <mybatis.version>3.0.4</mybatis.version>
    <shardingsphere-jdbc.version>5.5.1</shardingsphere-jdbc.version>
    <alipay-sdk-java.version>4.35.139.ALL</alipay-sdk-java.version>
    <maven.test.skip>true</maven.test.skip>   <!-- 顺带：默认跳过测试 -->
</properties>
```

于是 `novel-front/pom.xml` 里可以写 `<version>${jjwt.version}</version>`、`<version>${alipay-sdk-java.version}</version>`，改版本只改根 pom 一处。

**② dependencyManagement** —— 只「统一版本、不强制引入」；子模块声明同坐标时若没写版本，就用这里定的版本：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.java2nb</groupId>
            <artifactId>novel-common</artifactId>
            <version>${project.version}</version>
        </dependency>
        <!-- 引入 Spring AI 官方 BOM，管理所有 spring-ai-* 版本 -->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>1.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**③ 继承 spring-boot-starter-parent** —— 根 pom 的 `<parent>` 是 Spring Boot 官方父工程，它内部也是一个巨大的 BOM：`spring-boot-starter-web`、`spring-boot-starter-redis` 等 starter 全都不用手写版本号。

### 1.4 模块间依赖：front / crawl 怎么「引用」common

`novel-front` 与 `novel-crawl` 的 pom 都这样引入 common：

```xml
<dependency>
    <groupId>com.java2nb</groupId>
    <artifactId>novel-common</artifactId>
    <!-- 不写 version！由根 pom 的 dependencyManagement 统一提供 -->
</dependency>
```

好处：**换版本只改一处**；`novel-common` 里集中了 Web、MyBatis、分页、ShardingSphere、Redis、工具类等公共依赖，业务模块拿到的是「现成的骨架」。

### 1.5 重点：novel-admin 是一个例外模块

打开 `novel-admin/pom.xml`，你会发现它**和其他三个模块完全不是一路的**：

```xml
<!-- novel-admin/pom.xml 的 parent 是 Spring Boot 2.7.18，不是根 pom！ -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.7.18</version>
</parent>
```

对比：

| 对比项 | novel-common / front / crawl | novel-admin |
|---|---|---|
| 父工程 | 根 pom `novel`（→ Spring Boot **3.4.0**） | 直接继承 spring-boot-starter-parent **2.7.18** |
| 是否依赖 novel-common | front/crawl 依赖 | **不依赖**（自带 `com.java2nb.*.dao`、`*.domain` 包） |
| MyBatis | mybatis-spring-boot-starter 3.0.4 | mybatis-spring-boot-starter **1.1.1**（很老） |
| 其他代表性依赖 | 动态 SQL、PageHelper、Spring AI | springfox-swagger2 2.6.1、fastjson 1.2.83、shiro 1.11.0、jedis 2.9.0 |

**这个例外带来什么影响（学完要能讲）：**
- **javax vs jakarta**：Spring Boot 2.x 用 `javax.servlet.*`，3.x 用 `jakarta.servlet.*`。所以 admin 的代码（如 `HttpServletRequest`）与 front/crawl 的命名空间不同，两个体系互不通用。
- **为什么 admin 自带 dao/domain**：它不依赖 common，只能自带持久层，这也是第 1 课里「admin 的 `@MapperScan` 扫 `com.java2nb.*.dao`、而 front 扫 `com.java2nb.novel.mapper`」的根本原因。
- **为什么版本旧**：admin 更像「从老工程迁移过来还没升级」的模块。读代码时如果看到 admin 里 API 风格和 front 不一样，别奇怪，就是这个原因。

> 这个例外的教学价值：**看懂 pom 能帮你预判「模块间的代码为什么不一样」**，这是只读业务代码发现不了的。

### 1.6 打包与构建：pom 里藏着部署逻辑

三个可运行模块都配了 `spring-boot-maven-plugin`（打成**可执行 jar**），并配了 `maven-antrun-plugin` 在 `package` 阶段做「定制打包」：

- 把 `src/main/build/config`、启动脚本（`bin/*.sh|bat`）、`Dockerfile` 复制到 `target/build/`
- 打成 `target/build/xxx.zip` 便于分发
- `novel-front` 还会把 `templates`/`static` 同步到 `templates/green/`（第 1 课说的前端模版就是这么来的）

常用命令：

```bash
mvn clean package                 # 清理 + 打包（根 pom 已设 maven.test.skip=true，默认不跑测试）
mvn clean package -DskipTests     # 显式跳过测试
mvn dependency:tree               # 查看依赖树
```

### 1.7 仓库与镜像坑（pom 里直接写着）

根 pom 配置了阿里云仓库作为下载源：

```xml
<repositories>
    <repository>
        <id>ali</id>
        <url>https://maven.aliyun.com/repository/public</url>
        ...
    </repository>
</repositories>
```

**坑**（根 `pom.xml` 第 83-91 行注释原文说明）：如果本地 `settings.xml` 里配置了镜像，且 `<mirrorOf>` 是 `*`（拦截所有仓库），Maven 就不会再去 `io.github.xxyopen` 所在的 OSS 仓库下载，导致 `xxy-model/xxy-web/xxy-util` 等依赖解析失败。解决：把镜像的 `mirrorOf` 改成 `*,!oss`，或加 `central-repo` profile（根 pom 里已内置，可切换回中央仓库）。

---

## 二、动手练习（含验证标准）

> 做完一项勾一项。

### 练习 1：构建整个工程
- **目标**：亲自跑一次 Maven 构建，观察多模块的 reactor 顺序。
- **步骤**：在项目根目录执行 `mvn clean package`（或在 IDEA 右侧 Maven 面板点击根项目的 `clean` + `package`）。
- **验证标准**：输出中出现 reactor 顺序（common → front → crawl → admin），最终 `BUILD SUCCESS`；`novel-front/target/` 下出现 `novel-front-5.3.3.jar`。

### 练习 2：查看依赖关系
- **目标**：确认 front 依赖了 common。
- **步骤**：IDEA 打开 `novel-front/pom.xml` → 右侧 Maven 面板 → 展开 `Dependencies`，搜索 `com.java2nb`；或命令行执行 `mvn dependency:tree -pl novel-front`。
- **验证标准**：能看到 `com.java2nb:novel-common:jar:5.3.3`，且它下面还挂着 common 引入的 Web/MyBatis 等依赖（传递依赖）。

### 练习 3：找 admin 例外
- **目标**：亲手验证「admin 与其它模块不同源」。
- **步骤**：分别打开 `novel-front/pom.xml` 和 `novel-admin/pom.xml` 的 `<parent>` 标签，对比 groupId/artifactId/version；再搜 admin 的 pom 里有没有 `novel-common`。
- **验证标准**：能说出——admin 的 parent 是 spring-boot-starter-parent 2.7.18，且 admin 的依赖列表里**没有** novel-common。

---

## 三、本课小结

novel-plus 是标准的 **Maven 多模块聚合工程**：根 pom 用 `packaging=pom` + `<modules>` 组织四个模块，用 `properties` + `dependencyManagement` + 继承 starter-parent 三招统一版本；front / crawl 依赖 common 拿到公共骨架。**但 novel-admin 是例外**——它不继承根 pom、直接用 Spring Boot 2.7.18、不依赖 common，这解释了 admin 里 javax 命名、老版本依赖、自带 dao/domain 包等一切「看起来不一样」的地方。**读 pom 是读懂一个项目最快的方式之一。**

---

## 四、自测题

1. 【选择】根 pom.xml 的 `packaging` 是什么？（A. jar　B. war　C. pom　D. zip）
2. 【选择】`dependencyManagement` 的作用是？（A. 强制给所有模块加依赖　B. 只统一版本、不强制引入　C. 下载依赖　D. 打 zip 包）
3. 【选择】novel-admin 的 `<parent>` 是？（A. 根 pom `novel`　B. spring-boot-starter-parent 3.4.0　C. spring-boot-starter-parent 2.7.18　D. spring-boot-starter-parent 2.3.0）
4. 【简答】为什么 novel-front 引入 novel-common 不用写 `<version>`？
5. 【简答】`mirrorOf=*` 的镜像为什么会导致 `xxyopen` 相关依赖下载失败？怎么解决？

> 答案：1-C、2-B、3-C（见 1.2 / 1.3 / 1.5）、4-由根 pom 的 dependencyManagement 统一提供版本（见 1.4）、5-镜像拦截了所有仓库、`*,!oss` 或 central-repo profile（见 1.7）。

---

## 五、参考资源

- 本课程大纲：`Tutorial/课程大纲-30节课.md` → 第 3 课
- 技术栈路线：`doc/tech-stack-learning-roadmap.md` → 2.2 节 Maven
- 项目文件：根 `pom.xml`（第 83-91 行有 mirrorOf 坑的注释，值得一读）
- 官方文档：Maven POM 参考（maven.apache.org/pom.html）
