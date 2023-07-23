---
title: Unreal c++常见问题
date: 2022-3-24 15-51
categories:
- Unreal
tags:
- Unreal
catalog: true
---

# 类中静态成员变量 && 无法解析的外部符号：<https://blog.csdn.net/u012911202/article/details/103532273>

Unreal中使用Windows API：

D:\Windows Kits\10\include\10.0.20348.0\um\winnt.h(169): fatal error C1189: #error: "No Target Architecture"

![](assets/Unreal%20c++常见问题/Image.png)

winnt.h这个头文件依赖windows.h这个头文件

但是Unreal又不能直接 #include "windows.h"，因为一些API有冲突，Unreal在windows的api上包了一层

Unreal用windows的api要用这种形式

![](assets/Unreal%20c++常见问题/Image_1.png)

<https://forums.unrealengine.com/t/how-to-include-windows-h/308000>

其他相关：<https://stackoverflow.com/questions/4845198/fatal-error-no-target-architecture-in-visual-studio>

# error C4668: 没有将“_WIN32_WINNT_WIN10_TH2”定义为预处理器宏，用“0”替换“#if/#elif”

一般为Windows中的宏和UE4冲突所致，需要用如下头文件包裹冲突的头文件：

#include "Windows/AllowWindowsPlatformTypes.h"

#include "Windows/PreWindowsApi.h"

#include "冲突的头文件"

#include "Windows/PostWindowsApi.h"

#include "Windows/HideWindowsPlatformTypes.h"

[TODO]Speed Up Shader Compiling

<https://www.techarthub.com/seven-tricks-to-speed-up-shader-compilation-in-unreal-engine-4/>

<https://forums.unrealengine.com/t/turn-off-auto-compile-shaders/353474>

<https://realtimevfx.com/t/ue4-compiling-shaders-is-super-slow/3163/27>

<https://medium.com/gamedev4k/reducing-shader-compile-time-for-unreal-engine-landscape-a7a6c7e2ca20>

程序里include过，VS中不报错，但是编译报错：无法解析外部符号。

很可能在Build文件里面，没有把 依赖的相关模块 添加进来。

![](assets/Unreal%20c++常见问题/Image_2.png)

unable to load module:

<https://blog.ch-wind.com/ue4-transition-log/>

