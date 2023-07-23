---
title: Unity场景管理和切换
date: 2020-8-18 14-13
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## 关于yield return

对于yield return，目前我还无法深入理解其底层实现原理，无法看懂他编译成的IL代码。但是目前可以理解他的使用方法与机制。   
yield return会每次返回后记录返回的位置，待等待的时间到了之后，从返回的位置继续往下执行。

## API

### SceneManager.LoadScene

When using SceneManager.LoadScene, the scene **loads in the next frame** , that is it does not load immediately. This **semi-asynchronous** behavior can cause frame stuttering and can be confusing because load does not complete immediately.

Because loading is set to complete in the next rendered frame, calling SceneManager.LoadScene forces all previous AsyncOperations to complete, even if AsyncOperation.allowSceneActivation is set to false.

> 如果场景名称重复，路径不同：   
>  The given sceneName can either be the Scene name only, without the .unity extension, or the path as shown in the BuildSettings window still without the .unity extension. If only the Scene name is given this will load the first Scene in the list that matches. If you have multiple Scenes with the same name but different paths, you should use the full path.

#### 切换时相关Mono内存问题

场景切换的时候：Load a scene non-additively. This will destroy all Objects in the current scene and invoke `Resources.UnloadUnusedAssets` automatically.   
Destroy掉前一个场景中的GameObject，如果GameObject上挂载的Monobehaviour没有被其他地方引用的话，调用GC.Collect()会回收掉他占用的内存。

虽然GameObject被Destroy掉了， 如果Monobehaviour被其他在场景切换时无法销毁的对象所引用，那么其Mono层的对象是无法被回收的。比如：MonoBehaviour类中的某个函数注册了SceneManager类的sceneLoaded事件，那么这个对象就被SceneManager静态地引用了，该对象就无法销毁，Mono层的内存就无法释放。

### LoadSceneMode

(TODO: 是否会自动卸载，有待验证)   
使用Single模式，关闭已经加载的所有场景（不是卸载，卸载是另一个函数 —— UnloadSceneAsync()），只加载一个新场景，新场景被添加到SceneManager的目录中。

### 其他

SetActiveScene() 激活已加载的场景，如果场景未加载，返回false。

GetActiveScene() 获取已激活的场景。

CreateScene() 运行时创建一个新场景。

MergeScenes(SceneManagement.Scene sourceScene, SceneManagement.Scene destinationScene) 将源场景的内容合并到目标场景中，并删除源场景。 源场景根目录下的所有游戏对象都将移动到目标场景的根目录。需要注意的是，该函数具有破坏性 —— 合并完成后，源场景将被销毁。

MoveGameObjectToScene()   
将GameObject从其当前场景移动到新场景。   
只能将根游戏对象从一个场景移动到另一个场景。 这意味着要移动的GameObject不能是其场景中任何其他GameObject的子对象。 这仅适用于将GameObjects移动到已加载的场景（LoadSceneMode.Additive）。 如果要加载单个场景，请确保在要移动到新场景的GameObject上使用DontDestroyOnLoad，否则Unity会在加载新场景时删除它。

UnloadSceneAsync()   
销毁与给定场景关联的所有GameObject，并从SceneManager中移除场景。给定的场景名称可以是完整的场景路径，“构建设置”窗口中显示的路径，也可以是场景名称。   
注意：

  1. 由于它是异步的，因此无法保证完成时间。

  2. 资产目前尚未卸载。 为了释放资产内存，可以调用 Resources.UnloadUnusedAssets() 。

  3. 如果没有要加载的场景，则无法使用 UnloadSceneAsync() 。 

## 示例

### 进度条异步加载场景

AsyncOperation的progress（0-1）属性在allowSceneActivation 为false时，最大加载到0.9就会暂停，直到allowSceneActivation 为true时才会继续加载0.9-1.0的这10%。   
直到progress = 1.0时 isDone = true。

> 在Unity编辑器模式下是看不出来进度条正常变化的，只有导出项目后才能看到正常进度条

```csharp 

using System.Collections; 

using System.Collections.Generic; 

using UnityEngine; 

using UnityEngine.UI; 

using UnityEngine.SceneManagement; 

public class LoadSceneProgressBar : MonoBehaviour

{ 

private Slider _progress; 

void Awake()

{ 

_progress = GetComponent<Slider>(); 

} 

//使用协程

void Update()

{ 

if(Input.GetKeyDown(KeyCode.Space)) 

StartCoroutine(LoadScene()); 

} 

IEnumerator LoadScene()

{ 

//用Slider 展示的数值

int disableProgress = 0; 

int toProgress = 0; 

//异步场景切换

AsyncOperation op = SceneManager.LoadSceneAsync("MainScene_DayLight"); 

//不允许有场景切换功能

op.allowSceneActivation = false; 

//op.progress 只能获取到90%，最后10%获取不到，需要自己处理

while (op.progress < 0.9f) 

{ 

//获取真实的加载进度

toProgress = (int)(op.progress * 100); 

while (disableProgress < toProgress) 

{ 

++disableProgress; 

_progress.value = disableProgress / 100.0f;//0.01开始

yield return new WaitForEndOfFrame(); 

} 

} 

//因为op.progress 只能获取到90%，所以后面的值不是实际的场景加载值了，90~100之间的是假进度条。

toProgress = 100; 

while (disableProgress < toProgress) 

{ 

++disableProgress; 

_progress.value = disableProgress / 100.0f; 

yield return new WaitForEndOfFrame(); 

} 

op.allowSceneActivation = true; 

} 

} 

``` 

对于LoadSceneAsync，如果不使用yield return，也会在后台线程自动完成异步加载，只是无法一帧一帧获取当前的加载进度，无法实现加载完之后调用的逻辑。   
通过while+yield return的方式，是为了保证每帧执行一次while中的语句块，从而监控加载过程，并在加载结束后触发相应的逻辑。

### 从AssetBundle加载场景

```csharp 

// Load an assetbundle which contains Scenes.

// When the user clicks a button the first Scene in the assetbundle is

// loaded and replaces the current Scene.

using UnityEngine; 

using UnityEngine.SceneManagement; 

public class LoadScene : MonoBehaviour

{ 

private AssetBundle myLoadedAssetBundle; 

private string[] scenePaths; 

// Use this for initialization

void Start()

{ 

myLoadedAssetBundle = AssetBundle.LoadFromFile("Assets/AssetBundles/scenes"); 

scenePaths = myLoadedAssetBundle.GetAllScenePaths(); 

} 

void OnGUI()

{ 

if (GUI.Button(new Rect(10, 10, 100, 30), "Change Scene")) 

{ 

Debug.Log("Scene2 loading: " \+ scenePaths[0]); 

SceneManager.LoadScene(scenePaths[0], LoadSceneMode.Single); 

} 

} 

} 

``` 

### 分组加载卸载场景

```csharp 

/**************************************************************************

Copyright:@maxdong

Author: maxdong

Date: 2017-07-04

Description:加载关卡，可以分组加载和卸载。使用Unity版本为5.3.0.

因为里面使用了场景管理的一个类，这个类在5.3.0以上版本才添加的。

测试操作：使用空格键来切换场景，然后间隔5秒后才开始卸载。

**************************************************************************/

using UnityEngine; 

using System.Collections; 

using UnityEngine.SceneManagement; 

[System.Serializable] 

public class LevelOrder

{ 

[Header("每组关卡名称")] 

public string[] LevelNames; 

} 

public class ChangLevelsHasMain : MonoBehaviour

{ 

[Header("所有关卡列表")] 

public LevelOrder[] levelOrder; 

private static int index; 

private int totalLevels = 0; 

private int levelOrderLength; 

void Start ()

{ 

for (int i = 0; i < levelOrder.Length; i++) 

{ 

totalLevels += levelOrder[i].LevelNames.Length; 

} 

if (totalLevels != SceneManager.sceneCountInBuildSettings) 

{ 

} 

levelOrderLength = levelOrder.Length; 

} 

// Update is called once per frame

void Update ()

{ 

if (Input.GetKeyDown(KeyCode.Space)) 

{ 

bool isOk = LoadNextLevels(); 

if (isOk) 

{ 

InvokeRepeating("UnloadLastLevel", 2.0f, 5); 

} 

} 

} 

bool LoadNextLevels()

{ 

bool bResult = true; 

//index = index % levelOrderLength;

if (index < 0 || index >= levelOrderLength) 

{ 

bResult = false; 

return bResult; 

} 

int LoadTimes = levelOrder[index].LevelNames.Length; 

for (int i = 0; i < LoadTimes; i++) 

{ 

SceneManager.LoadSceneAsync(levelOrder[index].LevelNames[i], LoadSceneMode.Additive); 

} 

return bResult; 

} 

void UnloadLastLevel()

{ 

if (index == 0) 

{ 

index++; 

CancelInvoke("UnloadLastLevel"); 

return; 

} 

// 上一組的關卡

int TmpLast = (index - 1) >= 0 ? (index - 1) : levelOrderLength - 1; 

int LoadTimes = levelOrder[index].LevelNames.Length; 

for (int i = 0; i < LoadTimes; i++) 

{ 

Scene Tmp = SceneManager.GetSceneByName(levelOrder[index].LevelNames[i]); 

if (!Tmp.isLoaded) 

{ 

return; 

} 

} 

// 下一關卡全部加載完畢後，卸載之前關卡

for (int i = 0; i < levelOrder[TmpLast].LevelNames.Length; i++) 

{ 

SceneManager.UnloadScene(levelOrder[TmpLast].LevelNames[i]); 

} 

index++; 

CancelInvoke("UnloadLastLevel"); 

} 

} 

``` 

## Ref

<https://blog.csdn.net/Ha1f_Awake/article/details/93319307>

