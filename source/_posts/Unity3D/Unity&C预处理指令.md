---
title: Unity&C预处理指令
date: 2020-5-20 18-31
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---
# Unity&C#预处理指令

# Unity&C#预处理指令

## 预处理指令（条件编译）

预处理器指令指导编译器在实际编译开始之前对信息进行预处理。   
所有的预处理器指令都是以 # 开始。且在一行上，只有空白字符可以出现在预处理器指令之前。预处理器指令不是语句，所以它们不以分号（;）结束。   
C# 编译器没有一个单独的预处理器，但是，指令被处理时就像是有一个单独的预处理器一样。在 C# 中，预处理器指令用于在条件编译中起作用。与 C 和 C++ 不同的是，它们不是用来创建宏。一个预处理器指令必须是该行上的唯一指令。

```csharp 

#define 它用于定义一系列成为符号的字符。通过使用符号作为传递给 #if 指令的表达式，表达式将返回 true。

#undef 它用于取消定义符号。

#if 它用于测试符号是否为真。

#else 它用于创建复合条件指令，与 #if 一起使用。

#elif 它用于创建复合条件指令。

#endif 指定一个条件指令的结束。

#line 它可以让您修改编译器的行数以及（可选地）输出错误和警告的文件名。

#error 它允许从代码的指定位置生成一个错误。

#warning 它允许从代码的指定位置生成一级警告。

#region 它可以让您在使用 Visual Studio Code Editor 的大纲特性时，指定一个可展开或折叠的代码块。

#endregion 它标识着 #region 块的结束。

``` 

### Conditional特性

可以把输出日志的函数使用Conditional特性来标记上，只有在Unity编辑器中开启了指定的宏命令，这个输出日志的函数才能被编译，即可很方便地开关日志。   
`[Conditional("EnableLog")]`   
需要在Unity编辑器中添加上EnableLog宏命令，该方法才能被编译。

## Unity自带的一些宏定义

UNITY_EDITOR Unity编辑器   
UNITY_EDITOR_WIN Windows 操作系统.   
UNITY_EDITOR_OSX macos操作系统   
UNITY_STANDALONE_OSX 专门为macos（包括Universal, PPC，Intel architectures）平台的定义   
UNITY_STANDALONE_WIN 专门为windows平台的定义   
UNITY_STANDALONE_LINUX 专门为Linux平台的定义   
UNITY_STANDALONE 独立平台 (Mac OS X, Windows or Linux).   
UNITY_WII WII 游戏机平台   
UNITY_IOS iOS系统平台   
UNITY_IPHONE iPhone   
UNITY_ANDROID android系统平台   
UNITY_PS4 ps4平台   
UNITY_SAMSUNGTV 三星TV平台   
UNITY_XBOXONE Xbox One 平台   
UNITY_TIZEN Tizen 平台   
UNITY_TVOS Apple TV 平台   
UNITY_WSA #define directive for Universal Windows Platform. Additionally, NETFX_CORE is defined when compiling C# files against .NET Core and using .NET scripting backend.   
UNITY_WSA_10_0 #define directive for Universal Windows Platform. Additionally WINDOWS_UWP is defined when compiling C# files against .NET Core.   
UNITY_WINRT UNITY_WSA.   
UNITY_WINRT_10_0 UNITY_WSA_10_0   
UNITY_WEBGL #define directive for WebGL.   
UNITY_FACEBOOK faceBook平台(WebGL or Windows standalone).   
UNITY_ADS 调用广告方法，版本 5.2 以后   
UNITY_ANALYTICS 调用unity分析服务，版本5.2以后   
UNITY_ASSERTIONS 控制指令的过程

UNITY_5 unity5版本, 包含所有的5.x.y版本   
UNITY_5_0 Unity5.0版本,包含所有的5.0.x版本   
UNITY_5_0_1 Unity5.0.1版本

## 自定义宏定义

File - Build Settings - Player Settings - Other Settings   
多个用分号隔开

