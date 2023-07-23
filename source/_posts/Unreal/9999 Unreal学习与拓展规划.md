---
title: 9999 Unreal学习与拓展规划
date: 2021-12-17 18-56
categories:
- Unreal
tags:
- Unreal
catalog: true
---

# Unreal CI

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo.png)
<https://github.com/botman99/ue4-unreal-automation-tool>

## 基本自动化构建

### Source Code Automation

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_1.png)
<https://medium.com/@lifeexe/unreal-engine-ci-part-i-source-code-builds-8000ca1da723>

### Client Game Automation

学习路径：

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_2.png)
先把Mac打包走出来（直接打包 & 脚本自动打包）

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_3.png)
解答一个个困惑

    * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_4.png)
Cook和Build、Compile究竟是做什么

    * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_5.png)
AutomationTool和BuildTool之间的关系

    * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_6.png)
Graph的用法

    * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_7.png)
UAT的运行机制

  * 学习打包相关知识体系，整套工具的结构和用法

    * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_8.png)
从runUAT脚本看到UAT源码

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_9.png)
整理一套打包工具集

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_10.png)
进阶 - 分布式打包，效率提升

#### Windows

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_11.png)
<https://www.youtube.com/watch?v=2zkrhspvPls>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_12.png)
<https://patricevignola.com/post/automation-jenkins-unreal#automatically-build-your-game>

#### Mac iOS

![](assets/9999%20Unreal学习与拓展规划\\en_todo_13.png)
<https://imzlp.com/posts/1948/>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_14.png)
UAT参数 <https://zhuanlan.zhihu.com/p/41931214>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_15.png)

### Server + Client Automation

## 深入理解

Understanding Unreal Build Tool: https://ericlemes.com/2018/11/23/understanding-unreal-build-tool/

## 效率提升

### Distributed Build

FastBuild

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_16.png)
https://zhuanlan.zhihu.com/p/158400394

## CI体系

Jenkins, CI and Test-Driven Development:

https://unrealcommunity.wiki/jenkins-ci-amp-test-driven-development-6912tx0c

### Local Project Scan

### Unit Tests Automation

* * *

# Unreal游戏客户端技术

## 入门

见 《Unreal入门路线》 文档

### C++

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_17.png)
Compiling C++ https://ericlemes.com/2018/11/21/compiling-c-code/

## 进阶

Unreal资源检测工具学习：

* * *

# Unreal游戏服务端技术

* * *

# Unreal源码

https://zhuanlan.zhihu.com/p/160917246

# 资料集合

  * Exploring in UE4: <https://zhuanlan.zhihu.com/p/34256771>

  * 循迹研究室：https://imzlp.com/

  * UE知识库：https://ue5wiki.com/

  * UE博客：https://blog.csdn.net/u013412391/category_9736201.html

  * <https://romeroblueprints.blogspot.com/p/table-of-contents-c.html>

  * <https://zhuanlan.zhihu.com/p/49518229>

  * UE4:https://blog.csdn.net/jxyb2012/category_8644878.html

  * UEC++基础：https://www.zhihu.com/column/ue4cpp

  * Inside UE5: <https://zhuanlan.zhihu.com/p/24319968>

GC相关原理与经验：

https://zhuanlan.zhihu.com/p/219588301

https://zhuanlan.zhihu.com/p/341137213

https://www.cxymm.net/article/qq_29523119/119860186

https://blog.csdn.net/qq826364410/article/details/97691497

[https://www.wyfnote.com/2021/11/06/UE4/UE4CPP/Unreal%20GC%E8%BF%87%E7%A8%8B/](https://www.wyfnote.com/2021/11/06/UE4/UE4CPP/Unreal%20GC%E8%BF%87%E7%A8%8B)

# 个人问题

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_18.png)
Unreal加载，Unity可以把资源做成Prefab，打到AB里面，加载使用。Unreal资源如何打包？目前看来，蓝图相当于Prefab，Map当中会对Actor及其引用关系，进行序列化。不用蓝图的话，有没有类似于prefab、AB包的东西？

# 零碎知识学习

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_19.png)
反射系统使用：https://zhuanlan.zhihu.com/p/61042237

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_20.png)
Extending C++ To BP: <https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ClassCreation/CodeAndBlueprints/>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_21.png)
Architecture <https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_22.png)
Programming Basics <https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ProgrammingWithCPP/Basics/>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_23.png)
UE Containers:<https://docs.unrealengine.com/4.27/en-US/API/Runtime/Core/Containers/>

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_24.png)
UE对工程进行DEBUG：https://stonelzp.github.io/ue4-debug-your-project/

![](assets/9999%20Unreal学习与拓展规划\\en_todo_25.png)
Unreal 源码解析：https://edu.uwa4d.com/course-intro/0/374?purchased=false

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_26.png)
资源打包：https://imzlp.com/posts/22570/#more

UnrealBuildTool

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_27.png)
http://jazzlost.me/2019/11/24/Unreal-UBT-Modules/

![](assets/9999%20Unreal学习与拓展规划\\en_todo_28.png)
https://www.apude.com/blog/1712.html

![](assets/9999%20Unreal学习与拓展规划\\en_todo_29.png)
https://zhuanlan.zhihu.com/p/57186557

![](assets/9999%20Unreal学习与拓展规划\\en_todo_30.png)
UE研发基础命令：https://www.cnblogs.com/kekec/p/8684068.html

  * 
![](assets/9999%20Unreal学习与拓展规划\\en_todo_31.png)
UE Pipeline？ https://dev.epicgames.com/community/learning/courses/qEl/unreal-engine-technical-guide-to-linear-content-creation-pipeline-development/OP88/unreal-engine-overview-of-pipeline-development

