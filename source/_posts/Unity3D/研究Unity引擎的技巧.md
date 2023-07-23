---
title: 研究Unity引擎的技巧
date: 2020-6-4 11-12
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

# 调用Editor内部的函数

参考:  
https://www.xuanyusong.com/archives/4263（获取资源内存和硬盘大小)

Unity Editor实现的一些功能，调用了Editor本身的一些函数。这些函数可能没有作为API提供出来。如果想要调用，可以看Editor的源码：用dnSpy反编译一下，找到相关的代码与函数。  
然后利用反射，根据函数名调用相应函数。

此外，该方法提供了一个思路：想要深入理解UnityEditor的实现，就多看看Editor的包文件，反编译看看源码。一个是顺藤摸瓜，看相应功能的实现。一个是看包的整体结构组织，了解各个模块的功能以及实现，理解模块之间的关系。  
d  
一个小工具（用来调用内部函数）：

```csharp private static object InvokeInternalAPI(string type, string method, params object[] parameters) { var assembly = typeof(AssetDatabase).Assembly; var custom = assembly.GetType(type); var methodInfo = custom.GetMethod(method, BindingFlags.Public | BindingFlags.Static); return methodInfo != null ? methodInfo.Invoke(null, parameters) : 0; } ``` ```csharp [MenuItem("ProfilingTools/GetTextureMem")] public static void GetTextureMem() { Texture target = Selection.activeObject as Texture; Assembly editorAssembly = Assembly.Load("UnityEditor"); var type = editorAssembly.GetType("UnityEditor.TextureUtil"); MethodInfo methodInfo = type.GetMethod("GetStorageMemorySize", BindingFlags.Static | BindingFlags.Instance | BindingFlags.Public); Debug.Log("内存占用：" \+ EditorUtility.FormatBytes(UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong(Selection.activeObject))); Debug.Log("硬盘占用：" \+ EditorUtility.FormatBytes((int)methodInfo.Invoke(null, new object[] { target }))); } ``` 

# 监听Unity编辑器关闭的事件

```csharp using UnityEditor; public class Test { [InitializeOnLoadMethod] static void InitializeOnLoadMethod() { EditorApplication.wantsToQuit -= Quit; EditorApplication.wantsToQuit += Quit; } static bool Quit() { EditorUtility.DisplayDialog("我就是不让你关闭unity", "我就是不让你关闭unity", "呵呵"); return false; //return true表示可以关闭unity编辑器 } } ``` 
