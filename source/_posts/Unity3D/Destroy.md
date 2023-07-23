---
title: Destroy
date: 2020-6-19 17-02
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

Ref: <https://www.cnblogs.com/timeObjserver/p/7575035.html>

## 概述

UNITY Destroy()和DestroyImadiate()都不会立即释放对象内存

DestroyImadiate是立即将物体从场景hierachy中移除，并标记为 “null”，注意 是带引号的null。这是UNITY内部的一个处理技巧。关于这个技巧有很争议。

Destroy要等到帧末才会将物体从场景层级中移除并标记为”null”。

不管如何，二者都只是UNITY引擎层面的标记与处理，但在.NET底层，对象的内存都没有释放，只有手动GC.Collect()或等待NET去GC时才会释放掉对象内存。   
如果该对象在其他地方还有引用的话，GC也无法将对象的内存释放。

## 注意点

（1）obj并不会立即销毁，而是需要等待下一个Update更新，所以还是可以被print出来；   
（2）DestroyImmediate立即对对像进行销毁，print出来是null；   
（3）Destroy销毁场景中的物体，但内存中还存在，当令它需要销毁时，只是给一个标识。而内存中它依然是存在的，只有当内存不够，或一段时间没有再次被引用时（或者更多合理的条件满足），机制才会将它销毁并释放内存；   
（4）这样做的目的就是为了避免频繁对内存的读写操作。回收器会定时清理一次内存中引用计数为0的对象，很可能你的要销毁的对象在其他地方还有引用而你自己不清楚，直接销毁可能导致其他地方空引用错误；   
（5）建议使用平常Destroy函数，而不是DestroyImmediate函数；

## 测试

测试代码如下：点ADD按钮不断创建对象，点DEL按钮清除所有对象，通过观察进程内存数值来察看对象内存是否释放。

```csharp 

using System.Collections; 

using System.Collections.Generic; 

using System.Diagnostics; 

using UnityEngine; 

using UnityEngine.UI; 

public class MyGo : MonoBehaviour

{ 

byte[] data = new byte[83000]; 

} 

public class testad : MonoBehaviour { 

Transform objs; 

Text txt; 

Process proc; 

// Use this for initialization

void Start () { 

var btnadd = transform.Find("btnAdd").GetComponent<Button>(); 

btnadd.onClick.AddListener(OnClckAdd); 

var btndel = transform.Find("btnDel").GetComponent<Button>(); 

btndel.onClick.AddListener(OnClckDel); 

objs = transform.Find("objs"); 

txt = transform.Find("Text").GetComponent<Text>(); 

proc = Process.GetCurrentProcess(); 

} 

void OnClckAdd()

{ 

for (int i = 0; i < 20; ++i) 

{ 

var go = new GameObject(); 

go.AddComponent<MyGo>(); 

go.transform.SetParent(objs); 

} 

} 

void OnClckDel()

{ 

for (int i = objs.childCount - 1; i >= 0; i--) 

{ 

GameObject.DestroyImmediate(objs.GetChild(i).gameObject); 

} 

System.GC.Collect(); 

} 

// Update is called once per frame

float timer = 0; 

void Update () { 

if (timer > 0.5f) 

{ 

timer = 0; 

txt.text = ((int)(proc.WorkingSet64 / 1024)).ToString(); 

} 

timer += Time.deltaTime; 

} 

} 

``` 

