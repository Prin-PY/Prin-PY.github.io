---
title: Unity控制程序停止运行
date: 2020-5-21 19-32
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## 停止运行的Game

在编辑状态下，不点击停止播放键也一样能够控制程序停止运行

```csharp 

#if UNITY_EDITOR

UnityEditor.EditorApplication.isPlaying = false; 

#else

Application.Quit(); 

#endif

``` 

## Heading

