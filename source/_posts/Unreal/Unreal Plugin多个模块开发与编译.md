---
title: Unreal Plugin多个模块开发与编译
date: 2022-4-25 22-16
categories:
- Unreal
tags:
- Unreal
catalog: true
---

要写与模块名称相同的Module类，实现StartupModule、ShutdownModule函数，模块才能加载进来。

![](assets/Unreal%20Plugin多个模块开发与编译/Image.png)

模块的类型，如果要暴露给其他模块使用，要用 MODULENAME_API 来进行标记

![](assets/Unreal%20Plugin多个模块开发与编译/Image_1.png)

模块之间互相引用只要使用 PublicDependencyModuleNames.AddRange 即可。

至于说代码的头文件include，是否要添加PublicIncludePaths，取决于include的时候的方式，因为Paths是提供搜索的目标路径的，为了使搜索头文件的时候能搜索到。如果include命令保证头文件能搜索到就OK，如果搜索不到，就添加Public IncludePaths

Unreal C++代码的的Compile是以Module为单位的，可以在Unreal Editor的UI上，点击Compile，单独对某个模块进行编译。

![](assets/Unreal%20Plugin多个模块开发与编译/Image_2.png)

UI按钮的本质也是命令行语句，所以是存在语句用来编译单个模块的，只是现在还没有对RunUAT的命令行使用方法摸清楚，不知道如何编译单个模块。

只要Compile，就会把模块的所有代码都进行编译，至于说Private和Public源码是否保留，看我们如何设定。

Private和Public文件夹对于编译程序来说，并没有什么区别，只是对于开发者来设定的。Public一般是开源的部分。

Unreal中插件通常的使用方式是，把代码编译好成dll、so等后，留下来一部分头文件，开放给用户，用户就可以在自己的工程当中引用这个头文件了。

