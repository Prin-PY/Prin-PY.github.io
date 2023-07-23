---
title: 资源与内存(加载、卸载、Destroy)
date: 2020-4-28 11-31
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Unity文件，文件引用，meta详解

### Assets目录下常见的文件类型

#### 资源文件(ImportedAsset)

创建好的，并且不再修改的文件：FBX文件，贴图文件，音频文件，视频文件，动画文件   
导入时进行转化，每一个类型都对应一个AssetImporter   
点击这样的资源，在Inspector面板会出现设置界面

#### 代码文件

代码文件包括所有的代码文件，代码库文件，shader文件等，在导入时，unity会进行一次编译。

#### 序列化文件(Native Asset)

序列化文件通常是指unity能够序列化的文件，一般是unity自身的一些类型。比如prefab(预制体)，unity3d(场景)文件，asset(ScriptableObject)文件.mat文件(材质球)，这些文件能够在运行时直接反序列化为对应类的一个实例。

#### 文本文档

不是序列化文件，但是unity可以识别为TextAsset。   
很像资源文件，但是又不需要资源文件那样进行设置和转化。   
如txt、xml文件等等

#### 非序列化文件

非序列文件是Unity无法识别的文件，比如文件夹

#### Meta文件

meta文件在unity中的作用非常关键，它有2个作用

  * 定义在它同目录下，同名的非meta文件的唯一ID：GUID。而对于unity的序列化文件来说，引用的对象用的就是这个GUID。所以一旦meta中的GUID变更了，就要注意，它很可能引起一场引用丢失的灾难

  * 存储资源文件的ImportSetting数据。在上文中资源文件是有ImportSetting数据的，这个数据正数存储在meta文件中。ImportSetting中专门有存储Assetbundle相关的数据。这些数据帮助编辑器去搜集所有需要打包的文件并分门别类。所以每一次修改配置都会修改meta文件。

### Meta文件详解——Unity GUID/LocalID系统

meta文件——文本文档，YAML格式写的（序列化文件都是用这个格式写）

#### GUID

guid代表该文件，无论什么类型（甚至是文件夹）。   
通过GUID就可以找到工程中的这个文件，无论它在项目的什么位置。   
在编辑器中使用AssetDatabase.GUIDToAssetPath和AssetDatabase.AssetPathToGUID进行互转。

#### ImportSetting数据

根据不同的文件类型，它的数据是不同的ImportSetting数据（Inspector面板设置），比如上面的NativeFormatImporter，ModelImporter，AudioImporter等等。把一个文件和这个文件的meta文件从一个Unity工程复制到另一个Unity工程中，它的配置是不会变的。（将fbx和它的meta文件拷贝到另一个工程，不需要重新裁剪动画）

#### FileID（LocalID）

如果是一个图集，下面有若干个图片，那么就需要另外一个ID来表示，这就是LocalID（meta文件名为: FileID。）

  * 对于资源文件，非序列化文件，由于一般不会去更改源文件，所以FileID存储在meta文件中。

  * 对于序列化文件，自身数据里面会存储自身的FileID，也会记录所有子文件的FileID

> 所以在每次svn提交时如果发现有meta文件变更，一定要打开看一下。看看这个guid是否被更改。理论上是不需要更改的。

### 序列化文件详解——Unity文件引用系统

用sublime打开一个Scene文件(.unity)，   
大概的数据：

  * OcclusionCullingSettings裁剪数据（菜单Window->Occlusion面板中的数据）

  * RenderSettings（菜单Window->Lighting->Settings面板中的部分数据）

  * LightmapSettings（菜单Window->Lighting->Settings面板中的其他部分数据）

  * NavMeshSettings（菜单Window->Navigation面板中的数据）

  * 之后就是场景中的GameObject的数据

#### GameObject数据

Name就是Main Camera   
某个物体上有4个组件，每个组件有一个FileID，然后在需要引用时，使用这些FileID即可。实例化一个这样的GameObject时，只要依照次序，依次创建物体，组件，初始化数据并进行引用绑定即可在场景中生成一个实例。

> 在Inspector面板中的右上角点击，然后选择Debug转成Debug模式下的Inspector面板。   
>  在Hierarchy面板中选中Main Camera可以看到如图所示，所有的组件的LocalIdentfierInFile的值就是刚刚在Sublime中看到的数据

  * **InstanceID** 是unity中一个实例的ID。

  * 每一个Unity实例都会有一个InstanceID。在运行时，用UnityEngine.Object的GetInstanceID获取（《Unity编辑器下和运行时的加载过程》）

#### 组件数据

在GameObject之后就是组件数据。可以结合Unity中这个组件的面板来了解每一个数据的意义。

> 组件FlareLayer，在YAML里面只是一个Behaviour（所有Behaviour组件都看不到类型名字），怎么样才能知道他是一个FlareLayer？   
>  FileID左边我们看到一个124。每一个unity类型都有一个对应的数字。   
>  参考：<https://docs.unity3d.com/Manual/ClassIDReference.html>

任何一个文件都可以通过GUID找到，然后通过FileID找到它内部的子文件。所以这样就能识别出这个具体是什么类了。

#### Prefab数据

在YAML的最下面有一个数据是Prefab数据，保存了最重要的几个数据：   
Modification：每个组件的修改数据列表，但凡修改的数据，都会在这里体现。记录了：哪个资源（GUID）的哪个组件(FileID)的哪个成员(PropertyPath)的值(value)发生了改变。   
ParentPrefab：表示是哪一个Prefab。

![Alt text](资源与内存\(加载、卸载、Destroy\)
_files/289969-20180402204239871-1854753914.png)

## 资源导入

Unity automatically imports assets and manages various kinds of additional data about them for you, such as what import settings should be used to import the asset, and where the asset is used throughout your project. 

### What happens when Unity imports an Asset?

  1. A Unique ID is assigned   
This ID is used internally by Unity to refer to the asset which means the asset can be moved or renamed without references to the asset breaking.

> the editor frequently checks the contents of the Assets folder against the list of assets it already knows about.

  2. A .meta file is created

> If an asset loses its meta file (for example, if you moved or renamed the asset outside of Unity, without moving/renaming the corresponding .meta file), any reference to that asset will be broken. Unity would generate a new .meta file for the moved/renamed asset as if it were a brand new asset, and delete the old “orphaned” .meta file.

  3. The source asset is processed   
Unity reads and processes any files that you add to the Assets folder, converting the contents of the file to internal game-ready versions of the data. The actual asset files remain unmodified, and the processed and converted versions of the data are stored in the project’s **Library** folder.

> the Photoshop file format is convenient to work with and can be saved directly into your Assets folder, but hardware such as mobile devices and PC graphics cards can’t accept that format directly to render as textures. All the data for Unity’s internal representation of your assets is stored in the Library folder which can be thought of as similar to a cache folder. As a user, you should never have to alter the Library folder manually and attempting to do so may affect the functioning of the project in the Unity editor. However, it is always safe to delete the Library folder (while the project is not open in Unity) as all its data is generated from what is stored in the Assets and ProjectSettings folders. This also means that the Library folder should not be included in version control. 
> 
> Sometimes multiple assets are created from an import
> 
>   * A 3D file, such as an FBX, defines Materials and/or contains embedded Textures.
> 
>   * An image file imported as multiple sprites.
> 
>   * A 3D file contains multiple animation timelines, or has multiple separate clips defined within its animation import settings.
> 
> 

### The import settings can alter the processing of the asset

As well as the unique ID assigned to the asset, the meta files contain values for all the import settings you see in the inspector when you have an asset selected in your project window. For a texture, this includes settings such as the Texture Type, Wrap Mode, Filter Mode and Aniso Level.

If you change the import settings for an asset, those changed settings are stored in the .meta file accompanying the asset. The asset will be re-imported according to your new settings, and the corresponding imported “game-ready” data will be updated in the project’s Library folder.

## AssetDatabase

AssetDatabase is an API which allows you to access the assets contained in your project. Among other things, it provides methods to find and load assets and also to create, delete and modify them. The Unity Editor uses the AssetDatabase internally to keep track of asset files and maintain the linkage between assets and objects that reference them.

### Importing an Asset

### Loading an Asset

### File Operations using the AssetDatabase

### Using AssetDatabase.Refresh

When you have finished modifying assets, you should call AssetDatabase.Refresh to commit your changes to the database and make them visible in the project.

### CreateAssets & FindAssets & ScriptableObject

  1. 对于ScriptableObject，使用CreateInstance来创建Asset实例对象   
`testI = (ScriptObj)ScriptableObject.CreateInstance(typeof(ScriptObj));`

  2. 对于其他资源类型，使用new来创建对象

  3. 然后调用 `AssetDatabase.CreateAsset`函数，将实例对象作为资源存储在Assets路径当中。

  4. 最后使用`AssetDatabase.FindAssets`获取相应资源的GUID

  5. 由 `AssetDatabase.GUIDToAssetPath` 获取相应资源的路径。

```csharp 

// This script file has two CS classes. The first is a simple Unity ScriptableObject script.

// The class it defines is used by the Example class below.

// (This is a single Unity script file. You could split this file into a ScriptObj.cs and an

// Example.cs file which is more structured.)

using UnityEngine; 

using UnityEditor; 

public class ScriptObj : ScriptableObject

{ 

public void Awake()

{ 

Debug.Log("ScriptObj created"); 

} 

} 

// Use ScriptObj to show how AssetDabase.FindAssets can be used

public class Example

{ 

static ScriptObj testI; 

static ScriptObj testJ; 

static ScriptObj testK; 

[MenuItem("Examples/FindAssets Example two")] 

static void ExampleScript()

{ 

CreateAssets(); 

NamesExample(); 

LabelsExample(); 

TypesExample(); 

} 

static void CreateAssets()

{ 

testI = (ScriptObj)ScriptableObject.CreateInstance(typeof(ScriptObj)); 

AssetDatabase.CreateAsset(testI, "Assets/AssetFolder/testI.asset"); 

testJ = (ScriptObj)ScriptableObject.CreateInstance(typeof(ScriptObj)); 

AssetDatabase.CreateAsset(testJ, "Assets/AssetFolder/testJ.asset"); 

// create an asset in a sub-folder and with a name which contains a space

testK = (ScriptObj)ScriptableObject.CreateInstance(typeof(ScriptObj)); 

AssetDatabase.CreateAsset(testK, "Assets/AssetFolder/SpecialFolder/testK example.asset"); 

// an asset with a material will be used later

Material material = new Material(Shader.Find("Standard")); 

AssetDatabase.CreateAsset(material, "Assets/AssetFolder/SpecialFolder/MyMaterial.mat"); 

} 

static void NamesExample()

{ 

Debug.Log("*** FINDING ASSETS BY NAME ***"); 

string[] results; 

results = AssetDatabase.FindAssets("testI"); 

foreach (string guid in results) 

{ 

Debug.Log("testI: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

results = AssetDatabase.FindAssets("testJ"); 

foreach (string guid in results) 

{ 

Debug.Log("testJ: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

results = AssetDatabase.FindAssets("testK example"); 

foreach (string guid in results) 

{ 

Debug.Log("testK example: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

Debug.Log("*** More complex asset search ***"); 

// find all assets that contain test (which is all assets)

results = AssetDatabase.FindAssets("test"); 

foreach (string guid in results) 

{ 

Debug.Log("name:test - " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

} 

static void LabelsExample()

{ 

Debug.Log("*** FINDING ASSETS BY LABELS ***"); 

string[] setLabels; 

setLabels = new string[] {"wrapper"}; 

AssetDatabase.SetLabels(testI, setLabels); 

setLabels = new string[] {"bottle", "banana", "carrot"}; 

AssetDatabase.SetLabels(testJ, setLabels); 

setLabels = new string[] {"swappable", "helmet"}; 

AssetDatabase.SetLabels(testK, setLabels); 

// label searching:

// testI has wrapper, testK has swappable, so both have 'app'

// testJ has bottle, so have a label searched as 'bot'

string[] getGuids = AssetDatabase.FindAssets("l:app l:bot"); 

foreach (string guid in getGuids) 

{ 

Debug.Log("label lookup: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

} 

static void TypesExample()

{ 

Debug.Log("*** FINDING ASSETS BY TYPE ***"); 

string[] guids; 

// search for a ScriptObject called ScriptObj

guids = AssetDatabase.FindAssets("t:ScriptObj"); 

foreach (string guid in guids) 

{ 

Debug.Log("ScriptObj: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

guids = AssetDatabase.FindAssets("t:ScriptObj l:helmet"); 

foreach (string guid in guids) 

{ 

Debug.Log("ScriptObj+bottle: " \+ AssetDatabase.GUIDToAssetPath(guid)); 

} 

} 

} 

``` 

## AssetBundle

<https://blog.csdn.net/qq_35361471/article/details/82854560>

## 资源卸载（Unload & Destroy）

### Destroy

#### 概述

UNITY Destroy()和DestroyImadiate()都不会立即释放对象内存   
DestroyImadiate是立即将物体从场景hierachy中移除，并标记为 “null”，注意 是带引号的null。这是UNITY内部的一个处理技巧。关于这个技巧有很争议。   
Destroy要等到帧末才会将物体从场景层级中移除并标记为”null”。

不管如何，二者都只是UNITY引擎层面的标记与处理，但在.NET底层，对象的内存都没有释放，只有手动GC.Collect()或等待NET去GC时才会释放掉对象内存。   
如果该对象在其他地方还有引用的话，GC也无法将对象的内存释放。

#### 注意点

（1）obj并不会立即销毁，而是需要等待下一个Update更新，所以还是可以被print出来；   
（2）DestroyImmediate立即对对像进行销毁，print出来是null；   
（3）Destroy销毁场景中的物体，但内存中还存在，当令它需要销毁时，只是给一个标识。而内存中它依然是存在的，只有当内存不够，或一段时间没有再次被引用时（或者更多合理的条件满足），机制才会将它销毁并释放内存；   
（4）这样做的目的就是为了避免频繁对内存的读写操作。回收器会定时清理一次内存中引用计数为0的对象，很可能你的要销毁的对象在其他地方还有引用而你自己不清楚，直接销毁可能导致其他地方空引用错误；   
（5）建议使用平常Destroy函数，而不是DestroyImmediate函数；

#### 作用对象

GameObject、Component这样的在内存当中的实例，可以直接销毁，销毁掉后对硬盘上的资源是没有影响的。   
Load进来的资源文件（Texture等）不可以使用DestroyImmediate(obj)直接销毁。如果使用DestroyImmediate(obj, true)接口，可以销毁。对于序列化文件等Unity可以直接识别和接管的文件，相应的资源文件会销毁掉，而对于Texture这样的资源，Unity无法识别资源原始的图片，只能识别导入后加入Library中的文件，则会销毁Library中相应的资源，并断掉对该资源的引用（路径上就找不到该资源了）。而对于图片，由于原始文件没有被销毁，重新打开项目后，该图片会重新被Import进来。

总之，Destroy接口本身是不应该用来销毁资源的。

如果在游戏当中把资源Destroy掉，下次打开游戏，这个资源就没有了，加载不到了。

#### 测试

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

void Update () 

{ 

if (timer > 0.5f) 

{ 

timer = 0; 

txt.text = ((int)(proc.WorkingSet64 / 1024)).ToString(); 

} 

timer += Time.deltaTime; 

} 

} 

``` 

#### Resources.UnloadUnusedAssets

运行中卸载，可能是在帧末尾卸载

#### Resources.UnloadAsset()

对于场景当中的特定资源，如果相机照射到他或者在脚本中有对资源的引用的话就无法卸载。   
如果相机没有看到他，并且没有被引用到，那么该资源会在内存当中被卸载。而若下次引用到他，或者相机照射到他，那么该资源会被重新加载到内存当中。

#### EditorUtility.UnloadUnusedAssets

编辑器下的卸载资源接口。

## 资源卸载与内存管理问题的处理经验

  1. Editor中的脚本对物体的引用无法用Memory Profiler检测到，因为Editor脚本对MemoryProfiler是不可见的。

  2. 只要脚本中有对Texture等资源实例的引用，那么相应的资源就无法卸载掉。

  3. EditorUtility.UnloadUnusedAssets确实可以卸载没有被引用的资源对象，但是不会一调用就立即卸载掉，可能稍等一会儿才会卸载掉。所以，在这个函数调用过后立即检测内存，是看不出来卸载的效果的，过一小段时间后，再打印内存，就可以看到卸载的效果。根据对内存的监控可以判断：刚刚调用Unload资源函数的时候，内存不会立即释放，在下次加载资源的时候，会进行内存释放操作。

  4. 把加载进内存的对象直接Destroy掉，就不会占用内存，不需要调用Unload函数也可以。 如果把对资源的引用设置为null，不调用unload函数的话，资源会留在内存当中，只有调用unload之后，资源才会被卸载

## Ref

<https://www.cnblogs.com/CodeGize/p/8697227.html>   
<https://www.cnblogs.com/timeObjserver/p/7575035.html>   
<https://docs.unity3d.com/2017.2/Documentation/Manual/BehindtheScenes.html>

