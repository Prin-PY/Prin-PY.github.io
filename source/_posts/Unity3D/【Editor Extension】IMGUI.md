---
title: 【Editor Extension】IMGUI
date: 2021-1-26 18-12
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Introduction

An immediate mode graphic user interface (GUI), also known as IMGUI, is a graphical user interface design pattern which uses an immediate mode graphics library to create the GUI. via. Wikipedia

即时模式图形用户界面（IMGUI）代表了一种范例，其中用户界面的创建（对于客户端应用程序）和实现更简单（对于工具箱设计器）。

### 传统用户界面系统缓存状态的缺点

传统用户界面系统设计和使用的复杂性是由此类系统保持了各种状态引起的。程序员通常被要求在应用程* 序和用户界面之间来回主动地复制状态，以便用户界面反映应用程序的状态，反之，为了使用户界面中发生的更改影响应用程序的状态。UI系统的状态是实际状态的一份COPY/CACHE。

从客户端应用的角度看，UI更像是一堆对象的集合（通常称为widget），这些对象分装了需要和应用交互的各种状态。这个同步过程是双向的，为了让用户了解到当前应用的状态，状态需要从应用端转移到UI端；为了让应用知道当前用户的操作，状态需要从UI端转移到应用端。 

此外，通知应用程序用户与接口交互的方式（这反过来表明需要重新同步状态）通常采用回调的形式。这需要应用程序为感兴趣的任何低级交互实现“事件处理程序”，通常是通过手动或通过各种代码生成技巧将某些工具箱基类子类化；在任何一种情况下，都会使客户机应用程序的生命周期更加复杂。

### IMGUI

#### 优点

IMGUI通过要求应用程序实时显式传递可视化和交互所需的所有状态来消除这种状态同步。 用户界面只保留了为方便系统支持的每种小部件所需的功能所需的最小状态量。

Widget不再是对象，甚至可以说是不存在的。它们采用过程方法调用的形式，用户界面本身从有状态的对象集合变成了方法调用的实时序列。

这种实现方式的基础是实时应用程序循环的概念，也就是说，应用以实时的帧率处理逻辑和绘制（30 frames per second或者更高）。在游戏场景，这个是很常见的。

乍看起来，通过传递参数的方式实现看上去很冗余，但实际上并不是这样的。看上去会影响绘制性能。但是，对于现代的CPU和GPU而言，这个不是问题。

其优点在于简单和灵活。删除用户界面系统中的隐式状态缓存可以减少与缓存相关的bug的可能性，也完全消除了工具箱将小部件作为对象公开给客户机应用程序的需要。在逻辑上，小部件从对象变为方法调用。我们将看到，这从根本上改变了客户机应用程序处理用户界面实现的方式。

简单总结，IMGUI有以下优点：

  * 丝毫不需要分配内存，也即需要的内存为零！

  * 速度很快。即使使用非常复杂的UI并且只有单线程的情况下，大多数（如果不是全部）ImGUI在60fps（帧）的速度下运行没有任何问题。

  * 不需要对必须管理的对象进行创建和销毁操作。

  * 没有状态，因为没有对象来存储状态。

  * 基本不需要编制数据。

  * 没有需要注册或响应的事件或回调。

#### IMGUI的缺点

##### 可能需要更多的CPU

传统的GUI系统当元素有变化时，只需重新绘制局部元素。

ImGUI则相反，任何时候你想更改任何内容，整个图形用户界面就要重新绘制。即使是光标。以我们进入Excel示例，所有75个工具栏控件和300个单元格都将因为一个闪烁的光标而重新绘制。这是IMGUI的最坏情况。大量的CPU被浪费了。

##### 可访问性问题

通常GUI不保留任何数据，所以它可能做不了保留模式GUI能够做的那些事情。

##### 动画的支持性

大多数ImGUI都是无状态的，所以所有的动画都取决于应用程序。

## Unity IMGUI

IMGUI is a code-driven GUI system. It is driven by calls to the OnGUI function on any script which implements it. 

“Immediate Mode” refers to the way the IMGUI is created and drawn. To create IMGUI elements, you must write code that goes into a special function named OnGUI. The code to display the interface is executed every frame, and drawn to the screen. There are no persistent gameobjects   
other than the object to which your OnGUI code is attached, or other types of objects in the hierarchy related to the visual elements that are drawn.

### Unity GameObject-based UI system vs IMGUI

GameObject-based UI system has far better tools to work with the visual design and layout of the UI.

适用情况：Unity’s main GameObject-based UI system is used for normal in-game user interfaces that players might use and interact with.

IMGUI allows you to create a wide variety of functional GUIs using code. Rather than creating GameObjects, manually positioning them, and then writing a script that handles its functionality, you can do everything at once with just a few lines of code. The code produces GUI controls that are drawn and handled with a single function call.

### Controls

The Control defines the content

### GUIStyle & GUISkin

GUItyles define the appearance of a GUI Control. GUISkins are a collection of GUIStyles. 

### Layout

#### Fixed Layout & Automatic Layout

  * Fixed Layout makes sense to use when you have a pre-designed interface to work from. 

  * Automatic Layout makes sense to use when you don’t know how many elements you need up front, or don’t want to worry about hand-positioning each Control.

About Automatic Layout:

  * GUILayout is used instead of GUI

  * No Rect() function is required for Automatic Layout Controls

#### GUILayoutOptions

You can use GUILayoutOptions to override some of the Automatic Layout parameters. You do this by providing the options as the final parameters of the GUILayout Control.

### GUI vs EditorGUI

The difference between GUI and EditorGUI is primarily just their use case. GUI is used to display GUI items in game. GUI was the original way of creating Unity UI before their new canvas APIs. EditorGUI is used to create custom editors for your scripts and other editor customization.

One exception to that rule is that certain GUI classes are used for both. For instance, GUISkin and GUIStyle are used by both and their current values are accessed using GUI.skin regardless if used in game or in editor.

## 经验与思考

### 关于OnGUI调用逻辑的探究

Monobehaviour脚本的OnGUI在Play时确实是会每帧都调用，每帧都重新绘制内容。表现在使用如下脚本，Play时，字体会随着正弦函数不断连续变大变小。

```csharp 

// C# example

using UnityEngine; 

using System.Collections; 

public class Fontsize : MonoBehaviour

{ 

void OnGUI ()

{ 

//Set the GUIStyle style to be label

GUIStyle style = GUI.skin.GetStyle ("label"); 

//Set the style font size to increase and decrease over time

//This specific example requires that the default font (Arial) is loaded and marked as dynamic. You cannot change the size of any font that is not marked as dynamic.

style.fontSize = (int)(20.0f + 10.0f * Mathf.Sin (Time.time)); 

//the font does not smoothly change size, this is becauses there is not an infinite number of font sizes.

GUI.Label (new Rect (10, 10, 200, 80), "Hello World!"); 

} 

} 

``` 

但是在EditorWindow下，如果OnGUI中没有写EditorWindow.Repaint()的话，OnGUI并不会每帧都调用，字体大小不会自动连续地按照正弦曲线变大变小。只有当触发一定的事件时（比如点击窗口，在某个按钮上hover等），EditorWindow才会重新绘制，调用OnGUI。

如果OnGUI中主动调用Repaint()，则OnGUI会每帧都调用，原理还不明确。

### EditorGUI的一个BUG

EditorGUI有两个函数，BeginChangeCheck、EndChangeCheck()，用以检测特定范围内，UI元素的值是否发生改变。   
当Begin与Begin发生嵌套时，会

## Ref

<https://en.wikipedia.org/wiki/Immediate_mode_GUI>

<https://www.tangledrealitystudios.com/development-tips/gui-vs-guilayout-vs-editorgui-vs-editorguilayout-and-when-to-use-them/>

<https://www.cnblogs.com/grass-and-moon/p/13864696.html>   
<https://blog.csdn.net/csdnnews/article/details/90746003>

