---
title: ScriptableObject
date: 2020-6-9 17-02
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

> 文档：<https://docs.unity3d.com/ScriptReference/ScriptableObject.html>   
>  <https://docs.unity3d.com/Manual/class-ScriptableObject.html>

ScriptableObject类直接继承自Object类；它和MonoBehaviour是并列的，都继承自Object（但MonoBehaviour并不是直接继承自Object）

是一个 **数据容器** ，可以用来存储大量的数据，它是可序列化的。

## 作用

  1. 存储数据：在游戏运行时创建脚本化对象实例，然后可以将数据保存到本地（如果不保存，它会在游戏结束后销毁）；

  2. 减少内存：将数据存储在ScriptableObject对象中，在代码中可以进行引用，来减少工程以及游戏运行时因拷贝值所造成的内存占用；

> **ScriptableObject与预制体** ：当你有一个预制体，它附加了一些mono脚本，包含了一些数据，每次我们实例化预制体的时候它都会拷贝assets下原预制体的值生成一份自己的拷贝，然后我们可以修改场景内预制体的值而并不影响assets下预制体的值，这是prefab的特性，对于我们从一个prefab模板生成属性不同的游戏对象是很有用的，但是如果prefab里的脚本数据是不需要修改的，它就会造成很大的资源浪费，尤其在数据很多的时候；为了避免这种问题，我们可以在不需要修改prefab里的脚本数据时，考虑使用ScriptableObject来存储这些重复的数据，然后其它所有预制体都可以使用引用的方式来访问这份数据，这就意味着不管场景中实例了多少预制体，在内存中就只需要有一份数据；它所带给我们的启示就是， **当预制体中的脚本里有大量重复数据时，我们要想着将数据抽离，单独保存在本地**

## 特点

  1. **Unity编辑器外不可操作** ：仅在编辑器中才可以保存修改的数据（因为ScriptableObject对象虽然声明在UnityEngine中，但是它的Scriptable是通过UnityEditor命名空间下的类例如Editor类等来实现的），所以在部署构建的时候不可以用于存储游戏运行时更改的数据，但是可以使用之前存储好的数据。也就是ScriptableObject生成的数据资源文件 **在Editor外具有只读属性** ，如果你需要在游戏中修改数据并存储下来，就不推荐使用ScriptableObject了；

> 就像我们不可以在游戏运行时修改一个shader资源的代码、不可以修改一个纹理资源的像素内容一样，而在Unity Editor里可以修改ScriptableObject是因为Unity的编辑器对它格式的支持

  2. 继承自UnityEngine.Object，不必附着在对象上也无需/不能赋给Gameobject或Prefab

  3. 可以被serialize，可以在资源面板创建一个对应的.asset文件，把数据存储在资源文件中，通过属性面板可修改数值。该文件表示一个ScriptableObject的对象实例的序列化文件，退出之后也不会丢失。

  4. 本身是个类，可以引用，在项目之间共享

  5. 回调少 ：OnEnable 、OnDisable、OnDestroy

  6. persistent：当它被绑定到.asset文件或者AssetBundle等资源文件中的时候（它可以通过Resources.UnloadUnusedAssets来被unload出内存。可以通过脚本引用或其他需要的时候被再次load到内存）   
非persistent：通过CreateInstance<>来创建的时候（它可以通过GC被直接destroy掉（如果没有任何引用的话）。如果不想被GC的话，可以使用HideFlags.HideAndDontSave）

## 优点

  1. unity内置的一种储存容器

  2. PlayMode储存数据更改（再也不怕更改数据没保存了）   
3

## Method

```csharp 

//在游戏运行时创建一个Scriptable类型的实例，不使用时被GC回收；

//静态方法，使用了ScriptableObject类约束的泛型参数T

public static T CreateInstance<T>() where T : ScriptableObject; 

//实例化一个对象，返回一个实例；类似于GameObject的Instantiate()，其它函数也和GameObject类似

public static T Instantiate(T original); 

``` 

???   
ScriptableObject内部实现上也继承自MonoBehavior，它只有四个消息函数，Awake()、OnDestroy()、OnEnable()、OnDisable()；

## 使用方法

### MenuItem

需要指定创建的目录和资源名称，如果资源已经存在，则不会创建新资源；

```csharp 

public class MakeScriptableObject { 

[MenuItem("Assets/Create/My Scriptable Object")] 

public static void CreateMyAsset()

{ 

MyScriptableObjectClass asset = ScriptableObject.CreateInstance<MyScriptableObjectClass>(); 

AssetDatabase.CreateAsset(asset, "Assets/NewScripableObject.asset"); 

AssetDatabase.SaveAssets(); 

EditorUtility.FocusProjectWindow(); 

Selection.activeObject = asset; 

} 

} 

``` 

### CreateAssetMenu

可以在Assets下任意目录创建资源，而且可以创建多个资源；

```csharp 

[CreateAssetMenu(fileName = "data", menuName = "ScriptableObjects/SpawnManagerScriptableObject", order = 1)] 

public class SpawnManagerScriptableObject : ScriptableObject { 

public string prefabName; 

public int numberOfPrefabsToCreate; 

public Vector3[] spawnPoints; 

} 

``` 

在Assets下创建一个可编程对象资源，设置好所需数据；如果需要在其它脚本中获取该数据，是需要声明一个该类型变量，然后为其赋值或加载该数据资源；然后，就像使用用一个类中的公有变量一样使用即可；

```csharp 

public SpawnManagerScriptableObject spawnManagerValues; 

//spawnManagerValues.prefabName

``` 

### 动态创建

```csharp 

ScriptableObject.CreateInstance<MyScriptableObject >(); 

``` 

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

Debug.Log(" FINDING ASSETS BY NAME "); 

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

Debug.Log(" FINDING ASSETS BY LABELS "); 

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

Debug.Log(" FINDING ASSETS BY TYPE "); 

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

## 生命周期

ScriptableObject的生命周期和其他资源都是类似的：

当它是被绑定到.asset文件或者AssetBundle等资源文件中的时候，它就是persistent的，这意味着   
它可以通过Resources.UnloadUnusedAssets来被unload出内存   
可以通过脚本引用或其他需要的时候被再次load到内存   
如果是通过CreateInstance<>来创建的，它就是非persistent的，这意味着   
它可以通过GC被直接destroy掉（如果没有任何引用的话）   
如果不想被GC的话，可以使用HideFlags.HideAndDontSave

## 其他高级应用Demo

<https://blog.csdn.net/candycat1992/article/details/52181814>

### 保存信息

step1.创建你用于共享数据的类（例如EnemyData）

```csharp 

using UnityEngine; 

public class EnemyData: ScriptableObject

{ 

public string name; 

public Color thisColor; 

public Vector3[] spawnPoints; 

} 

``` 

step2.新建一个脚本扩展Editor,使编辑器能够创建自定义的ScriptableObject对象

```csharp 

using UnityEngine; 

using UnityEditor; 

//新建一个Editor文件夹，放在里面

public class MakeEnemyData{ 

[MenuItem("Assets/Editor/Scriptable Object")] //定义了如何新建的路径

public static void CreateMyAsset()

{ 

//将EnemyData创建为asset

EnemyData asset = ScriptableObject.CreateInstance<EnemyData>(); 

//设置新创建的NewScripableObject文件的初始路径

AssetDatabase.CreateAsset(asset, "Assets/NewScripableObject.asset"); 

AssetDatabase.SaveAssets(); 

EditorUtility.FocusProjectWindow(); 

Selection.activeObject = asset; 

} 

} 

``` 

step3. 在需要引用的脚本中引用

```csharp 

using UnityEngine; 

public class EnemyAI : MonoBehaviour { 

public EnemyData data; //data配置的数据就可以被所有相同种类的怪物共享，节省内存

} 

``` 

### 用作配置文件

```csharp 

[CreateAssetMenu] 

public class GameSettings : ScriptableObject

{ 

[Serializable] 

public class PlayerInfo

{ 

public string Name; 

public Color Color; 

... 

} 

public List<PlayerInfo> players; 

private static GameSettings _instance; 

public static GameSettings Instance 

{ 

get

{ 

if (!_instance) 

_instance = Resources.FindObjectsOfTypeAll<GameSettings>().FirstOrDefault(); 

#if UNITY_EDITOR

if (!_instance) 

InitializeFromDefault(UnityEditor.AssetDatabase.LoadAssetAtPath<GameSettings>("Assets/Test game settings.asset")); 

#endif

return _instance; 

} 

} 

public int NumberOfRounds; 

public static void LoadFromJSON(string path)

{ 

if (!_instance) DestroyImmediate(_instance); 

_instance = ScriptableObject.CreateInstance<GameSettings>(); 

JsonUtility.FromJsonOverwrite(System.IO.File.ReadAllText(path), _instance); 

_instance.hideFlags = HideFlags.HideAndDontSave; 

} 

public void SaveToJSON(string path)

{ 

Debug.LogFormat("Saving game settings to {0}", path); 

System.IO.File.WriteAllText(path, JsonUtility.ToJson(this, true)); 

} 

public static void InitializeFromDefault(GameSettings settings)

{ 

if (_instance) DestroyImmediate(_instance); 

_instance = Instantiate(settings); 

_instance.hideFlags = HideFlags.HideAndDontSave; 

} 

#if UNITY_EDITOR

[UnityEditor.MenuItem("Window/Game Settings")] 

public static void ShowGameSettings()

{ 

UnityEditor.Selection.activeObject = Instance; 

} 

#endif

... 

} 

``` ```csharp 

public class MainMenuController : MonoBehaviour

{ 

public GameSettings GameSettingsTemplate; 

... 

public string SavedSettingsPath { 

get { 

return System.IO.Path.Combine(Application.persistentDataPath, "tanks-settings.json"); 

} 

} 

void Start () { 

if (System.IO.File.Exists(SavedSettingsPath)) 

GameSettings.LoadFromJSON(SavedSettingsPath); 

else

GameSettings.InitializeFromDefault(GameSettingsTemplate); 

foreach(var info in GetComponentsInChildren<PlayerInfoController>()) 

info.Refresh(); 

NumberOfRoundsSlider.value = GameSettings.Instance.NumberOfRounds; 

} 

public void Play()

{ 

GameSettings.Instance.SaveToJSON(SavedSettingsPath); 

GameState.CreateFromSettings(GameSettings.Instance); 

SceneManager.LoadScene(1, LoadSceneMode.Single); 

} 

... 

} 

``` 

## Ref:

<https://blog.csdn.net/qq_36383623/article/details/99649941>   
<https://blog.csdn.net/candycat1992/article/details/52181814>

