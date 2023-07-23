---
title: Profiler使用技巧
date: 2020-8-20 23-37
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

```csharp using UnityEngine; using System.Collections; using UnityEngine.Profiling;public class ExampleClass : MonoBehaviour { void Start() { Profiler.logFile = "mylog"; //Also supports passing "myLog.raw" Profiler.enableBinaryLog = true; Profiler.enabled = true; // Optional, if more memory is needed for the buffer Profiler.maxUsedMemory = 256 * 1024 * 1024; // ... // Optional, to close the file when done Profiler.enabled = false; Profiler.logFile = ""; // To start writing to a new log file Profiler.logFile = "myOtherLog"; Profiler.enabled = true; // ... } } ``` 
