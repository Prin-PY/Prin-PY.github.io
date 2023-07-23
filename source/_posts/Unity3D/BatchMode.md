---
title: BatchMode
date: 2020-6-16 18-51
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## 使用原理

### DOS

DOS是Disk Operation System(磁盘操作系统）的简称，是个人计算机上的一类操作系统。它直接操纵管理硬盘的文件，一般都是黑底白色文字的界面。   
DOS就是人与机器的一座桥梁，是罩在机器硬件外面的一层“外壳”，只需通过一些接近于自然语言的DOS命令，就可以轻松地完成绝大多数对机器的日常操作。   
此外，DOS还能有效地管理各种软硬件资源，对它们进行合理的调度，所有的软件和硬件都在DOS的监控和管理之下，有条不紊地进行着自己的工作，但是在操作不慎情况下也会死机。   
**MS-DOS** 是MicroSoft-dos，它不是纯DOS，是基于Windows的DOS程序，在功能上类似于DOS，但是不一样。   
最新的Windows操作系统中，MS-dos的核心依然存在，只是加上Windows当作系统的图形界面。   
微软图形界面操作系统 Windows NT 问世以来，DOS是一个 **后台程序** 的形式出现的。名为 **Windows命令提示符** 。可以通过点击运行- **CMD** 进入。

#### DOS命令

DOS命令行不许要去专门当做一门语言学习，你只需要根据自己的需求百度一下命令行的使用方式即可。

### Batch(.bat文件)

**批处理(Batch)** ，也称为 **批处理脚本** 。通常被认为是一种简化的脚本语言，也称作宏。它应用于DOS和Windows系统中。   
它是由DOS或者Windows系统内嵌的命令解释器（通常是COMMAND. COM或者CMD.EXE）解释运行。类似于Unix中的Shell脚本。批处理文件具有.bat或者.cmd的扩展名，其最简单的例子，是逐行书写在命令行中会用到的各种命令。   
**使用** ：在“命令提示”下键入批处理文件的名称，或者双击该批处理文件，系统就会调用Cmd.exe运行该批处理程序。   
**运行** ：运行批处理程序时，首先扫描整个批处理程序，然后从第一行代码开始向下逐句执行所有的命令，直至程序结尾或遇见exit命令或出错意外退出。

> 批处理程序虽然是在命令行环境中运行，但不仅仅能使用命令行软件，任何当前系统下可运行的程序都可以放在批处理文件中运行。

#### 命令

##### echo 命令

语法: echo [{on|off}] [message]   
Sample：@echo off / echo hello world

打开回显或关闭请求回显功能，或显示消息。如果没有任何参数，echo命令将显示当前回显设置。   
在实际应用中我们会把这条命令和重定向符号（也称为管道符号，一般用> >> ^）结合来实现输入一些命令到特定的文件中，例如：

```csharp 

echo test>test.txt 

# 会创建一个名为"test"的文本文件，并将"test"输入到文本文件中。 

``` 

在批处理文件的开头，通常有：   
echo off   
原因是”@”可以将本行的命令关闭回显，搭配”echo off”就可以不显示”echo off”的回显了。

##### rem 命令

语法：Rem [注释内容]   
Sample：Rem 你好。

注释命令，类似于在C语言中的/ _——–_ /，它并不会被执行，只是起一个注释的作用，只有在编辑批处理时才会被看到，主要用于方便修改。   
:: 也具有rem的功能   
但::和rem还是有区别的，当关闭回显时，rem和::后的内容都不会显示。   
但是当打开回显时，rem后的内容会显示出来，然而::后的内容仍然不会显示。

##### pause

暂停命令。运行 Pause 命令时，将显示下面的消息：   
Press any key to continue…（或：请按任意键继续…)

##### call

##### start

##### goto

##### set

#### 符号

### 其他概念

Bash(Bourne-Again SHell): Unix shell的一种，能运行于大多数类Unix系统的操作系统之上，包括Linux与Mac OS X v10.4都将它作为默认shell。   
是一个命令处理器，通常运行于文本窗口中，并能执行用户直接输入的命令。Bash还能从文件中读取命令，这样的文件称为脚本。

### Unity Editor拓展

放在工程目录下Assets/Editor文件下的方法都是对Unity引擎编辑器的拓展，一般常见的插件都会编写一部分编辑器拓展代码来自定义插件的Inspector面板等其他操作。

### Editor方法触发方式

#### MenuItem

#### EditorWindow->Button

```csharp 

using UnityEditor; 

using UnityEngine; 

public class MyClass : EditorWindow

{ 

// 重写window面板

private void OnGUI()

{ 

if(GUILayout.Button("MyFunc1")) 

{ 

MyFunc1(); 

} 

} 

// 打开窗口

[MenuItem("My Tools/My Window")] 

private static void OpenMyWindow()

{ 

GetWindow<MyClass> (true, "My Window"); 

} 

[MenuItem("My Tools/MyFunc1")] 

private static void MyFunc1()

{ 

//..你的操作

Debug.Log ("你的操作"); 

} 

} 

``` 

#### 利用批处理来调用

更多Unity Command line arguments：<https://docs.unity3d.com/Manual/CommandLineArguments.html>

> 最新Unity支持直接用.bat脚本直接导出linux、MacOS、Window的应用，暂时不支持Android和IOS等其它终端的输出。

```csharp 

using UnityEditor; 

public class MyWindow : EditorWindow

{ 

public static void MyFunc1()

{ 

Debug.Log("MyFunc1 Operation"); 

} 

} 

``` ```csharp 

rem 发布工具

@echo off 

echo 启动 Unity.exe 请稍后... 

start /min D:\Unity\Editor\Unity.exe -batchmode -projectPath D:\MyProject\BatchProject -executeMethod MyClass.MyFunc1 

Pause

taskkill /f /im unity.exe 

``` 

##### 命令介绍

echo 为DOS编程中一种显示消息的方法

start DOS编程中用于启动应用程序的命令   
-batchmode 是Unity提供的Command line arguments中较为常用的一种，它是后台运行Unity，不显示Unity界面，这对于把机械的工作交给策划？美术？是极其重要的。   
在-batchmode下运行Unity。这应该始终与其他命令行参数一起使用，因为 **它确保没有出现弹出窗口，并且不需要任何人为干预** 。执行脚本代码期间发生异常时，资产服务器更新失败或其他失败的操作，Unity立即退出并返回代码1。   
请注意，在批处理模式下，Unity将其日志输出的最小版本发送到控制台。但是，日志文件仍然包含完整的日志信息。在编辑器打开相同的项目时以批处理模式打开项目不受支持; Unity的一个实例只能一次运行。

-projectPath 指定项目的路径

-executeMethod(ClassName.MethodName) 调用Unity编辑器某个类型中的某个方法

一旦Unity启动，项目打开，并且执行了可选的Asset Server更新之后，执行静态方法。这可以用于执行持续集成，执行单元测试，构建或准备数据等任务。要从命令行进程返回错误，请抛出异常，导致Unity退出代码1，或者使用非零返回代码调用EditorApplication.Exit。要传递参数，将它们添加到命令行并使用函数检索它们System.Environment.GetCommandLineArgs。要使用-executeMethod，您需要将封闭的脚本放在编辑器文件夹中。要执行的方法必须定义为static。

Ref: <https://blog.csdn.net/qq_29579137/article/details/76598929>

