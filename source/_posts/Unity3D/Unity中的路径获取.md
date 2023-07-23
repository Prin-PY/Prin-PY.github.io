---
title: Unity中的路径获取
date: 2020-5-18 11-16
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## AssetDatabase

### 获取选中资源

```csharp 

[MenuItem("Tools/GetSelectPaths")] 

public static void Execute()

{ 

string[] strs = Selection.assetGUIDs; 

var curPath = System.IO.Directory.GetCurrentDirectory();//获取当前根目录

foreach (var item in strs) 

{ 

string path = AssetDatabase.GUIDToAssetPath(item); 

Debug.Log(curPath+"/"+path); 

} 

} 

``` 

### Active/Deactive选中物体

```csharp 

[MenuItem("Example/Toggle Active of Selected %i")] 

static void DoToggle()

{ 

Object[] activeGOs = Selection.GetFiltered( 

typeof(GameObject), 

SelectionMode.Editable | SelectionMode.TopLevel); 

foreach (GameObject obj in activeGOs) 

{ 

obj.SetActive(!obj.activeSelf); 

} 

} 

``` 

### 遍历所有文件

```csharp 

private readonly string configJsonPath = AssetDatabase.GetAllAssetPaths() 

.FirstOrDefault(p => p.EndsWith("uwascan_ruleconfig.json")); 

``` 

## Application

获取路径：”………………../Assets”

```csharp 

string path = Application.dataPath; 

``` 

### 遍历所有文件夹 (待学习)

```csharp 

//遍历所选文件夹，查找该文件夹以及子文件夹中 后缀为 .prefab的文件路径

using UnityEngine; 

using System.Collections; 

using System.Collections.Generic; 

using UnityEditor; 

using System.IO; 

public class CameraMove : MonoBehaviour { 

// 在菜单来创建 选项 ， 点击该选项执行搜索代码

[MenuItem("Tools/遍历项目所有文件夹")] 

static void CheckSceneSetting()

{ 

List<string> dirs = new List<string>(); 

GetDirs(Application.dataPath, ref dirs); 

} 

//参数1 为要查找的总路径， 参数2 保存路径

private static void GetDirs(string dirPath, ref List<string> dirs)

{ 

foreach (string path in Directory.GetFiles(dirPath)) 

{ 

//获取所有文件夹中包含后缀为 .prefab 的路径

if (System.IO.Path.GetExtension(path) == ".prefab") 

{ 

dirs.Add(path.Substring(path.IndexOf("Assets"))); 

Debug.Log(path.Substring(path.IndexOf("Assets"))); 

} 

} 

if (Directory.GetDirectories(dirPath).Length > 0) //遍历所有文件夹

{ 

foreach (string path in Directory.GetDirectories(dirPath)) 

{ 

GetDirs(path, ref dirs); 

} 

} 

} 

} 

``` 

