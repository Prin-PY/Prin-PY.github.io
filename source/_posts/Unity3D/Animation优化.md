---
title: Animation优化
date: 2020-7-18 0-24
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

**标签：**|  _优化_  

## 优化方案

  1. Rig->Animation Type:改为Generic

  2. Animations->Anim.Compression:Optimal

  3. 其他高级方式

## 曲线数据存储与压缩

### 存储方式

#### Stream(流)

Use the “stream” method of storing data (values with time and tangent data for curved interpolation).   
（保留时间和切线数据进行 **曲线插值** ）   
This data occupies significantly **more memory** than the “dense” method.

> Streaming curves are very fast to decompress in the average use case.

#### Dense(密集的)

Optimize animation curves using the “dense” method of storing data (discrete values which are interpolated between linearly).   
（离散数值之间的 **线性差值** ）   
不含有切线数据，使用较少内存   
This method uses less significantly less memory than the “stream” method.   
与“流”方法相比，此方法使用的内存要少得多。

#### Constant

Curves are optimised as constant (unchanging) values.   
Unity selects this automatically if your animation files contain curves with unchanging values.

### Compression方式

Unity引擎对导入的Clip提供三种压缩格式，Off、KeyframeReduction和Optimal。其中Off表示不压缩，Keyframe Reduction表示使用关键帧进行处理，Optimal则表示Unity引擎会根据动画曲线的特点来自动选择一个最优的压缩方式。

#### Off

存储方式：Stream

不压缩，官方不推荐

> Unity文档: This means that Unity doesn’t reduce keyframe count on import. Disabling animation compression leads to the highest precision animations, but slower performance and bigger file and runtime memory size. It is generally not advisable to use this option - if you need higher precision animation, you should enable keyframe reduction and lower allowed Animation Compression Error values instead.

#### Keyframe Reduction

存储方式：Stream   
压缩方式：关键帧缩减算法

##### Keyframe Reduction算法

Basically key frame reduction will simply **go through all key frames in your animation, and evaluate the animation curves with and without that key, and if the difference is smaller then some defined delta, the key is removed.**

**error tolerance(误差宽容度，容错值)** 或者称为 **error threshold(误差阈值)**   
值越小动画的精度越高，如果默认值的表现效果不过好，可以通过减小容错值来调。

  * Rotation Error 角度值

  * Position Error 百分比值

  * Scale Error 百分比值

Unity compares the original curve to what the curve looks like after removing a specific keyframe and applies this test：   
OriginalValue - ReducedValue > OriginalValue * percentageOfError   
Unity removes a keyframe if the delta between the original value and the reduced value is less than the original value multiplied by the error tolerance percentage.

#### Optimal

存储方式：(Unity官方)Unity will use a heuristic algorithm to determine whether it is best to use the **dense** or **stream** method to store the data for each curve.   
(笔者推测，可能对于unchanging的值做优化处理，使用constant方式存储)   
压缩方式：Unity decide how to compress, either by **keyframe reduction** or by using **dense format**.

If a track is very short or very noisy (which could happen with motion capture clips or baked simulations), the key reduction algorithm might not give appreciable gains and it is possible that a dense curve might end up having a smaller memory footprint than a streaming curve. 

> Unity官方：   
>  If your animation clips are imported with “Anim Compression” set to “Optimal” in the Animation import reference, Unity will use a heuristic（启发式的） algorithm to determine whether it is best to use the **dense** or **stream** method to **store the data for each curve**.

### UWA性能对比实验

<https://blog.uwa4d.com/archives/Loading_AnimationClip.html>

  1. Optimal压缩方式确实可以提升资源的加载效率，无论是在高端机、中端机还是低端机上；

  2. 硬件设备性能越好，其加载效率越高。但随着设备的提升，Keyframe Reduction和Optimal的加载效率提升已不十分明显；

  3. Optimal压缩方式可能会降低动画的视觉质量，因此，是否最终选择Optimal压缩模式，还需根据最终视觉效果的接受程度来决定。

### 总结

从性能的角度来看，Optimal的方式内存占用是最低的，是我们最推荐的方案，但是可能会降低动画的视觉质量。Off是不压缩，Unity官方都不推荐的。Keyframe Reduction内存稍高于Optimal，在内存性能和效果上算是折中的方案，用户手动设置Keyframe Reduction问题不大。

## 优化方法

### 1\. 去掉AnimationClip中的无效曲线：例如ScaleCurve

```csharp 

using UnityEngine; 

using UnityEditor; 

using System.Collections.Generic; 

public class RemoveCurve : AssetPostprocessor

{ 

void OnPostprocessModel(GameObject g)

{ 

Apply(g); 

} 

void Apply(GameObject g)

{ 

List<AnimationClip> animationClipList = new List<AnimationClip>(AnimationUtility.GetAnimationClips(g)); 

if (animationClipList.Count == 0) 

{ 

AnimationClip[] objectList = UnityEngine.Object.FindObjectsOfType(typeof(AnimationClip)) as AnimationClip[]; 

animationClipList.AddRange(objectList); 

} 

foreach (AnimationClip theAnimation in animationClipList) 

{ 

foreach (EditorCurveBinding theCurveBinding in AnimationUtility.GetCurveBindings(theAnimation)) 

{ 

string name = theCurveBinding.propertyName.ToLower(); 

if (name.Contains("scale")) 

{ 

AnimationUtility.SetEditorCurve(theAnimation, theCurveBinding, null); 

} 

} 

} 

} 

} 

``` 

### 2\. 压缩AnimationClip文件float的精度

```csharp 

public static bool CompressAnimationClip(Object o)

{ 

string animationPath = AssetDatabase.GetAssetPath(o); 

try

{ 

//AnimationClip clip = GameObject.Instantiate(o) as AnimationClip;

AnimationClip clip = o as AnimationClip; 

AnimationClipCurveData[] curves = null; 

curves = AnimationUtility.GetAllCurves(clip); 

Keyframe key; 

Keyframe[] keyFrames; 

for (int ii = 0; ii < curves.Length; ++ii) 

{ 

AnimationClipCurveData curveDate = curves[ii]; 

if (curveDate.curve == null || curveDate.curve.keys == null) 

{ 

//Debug.LogWarning(string.Format("AnimationClipCurveData {0} don't have curve; Animation name {1} ", curveDate, animationPath));

continue; 

} 

keyFrames = curveDate.curve.keys; 

for (int i = 0; i < keyFrames.Length; i++) 

{ 

key = keyFrames[i]; 

key.value = float.Parse(key.value.ToString("f3")); 

key.inTangent = float.Parse(key.inTangent.ToString("f3")); 

key.outTangent = float.Parse(key.outTangent.ToString("f3")); 

keyFrames[i] = key; 

} 

curveDate.curve.keys = keyFrames; 

clip.SetCurve(curveDate.path, curveDate.type, curveDate.propertyName, curveDate.curve); 

} 

//AssetDatabase.CreateAsset(clip, animationPath);

Debug.Log(string.Format(" CompressAnimationClip {0} Success !!!", animationPath)); 

return true; 

} 

catch(Exception e) 

{ 

Debug.LogError(string.Format("CompressAnimationClip Failed !!! animationPath : {0} error: {1}", animationPath, e)); 

return false; 

} 

} 

``` 

## 其他内容

### optimize gameobject

针对Mecinam新版动画系统的优化选项，默认情况下会将动画网格下的所有骨骼结点隐藏，但是，你可以通过“Extra Transform to Expose”查看你想通过脚本获取的骨骼结点，这样既可以提升该角色的动画模块性能，又可以达到获取某个关键结点的需求。不过这种方式获得的骨骼节点是只读的，如果想要对其中的属性进行改变比如换装，就不可以开启这个选项。

### multithreaded rendering

多线程渲染，将主线程的一部分渲染工作移到另一个线程里执行，Android平台下才有的优化渲染设置，但是对半透明物体支持不好，项目中需要进行测试来决定开不开启。

### Animation Type

Legacy Generic Humaniod   
Legacy 老版动画系统   
Generic 适合非人型动画   
Humaniod 适合人型动画，可以动画重定向   
cpu耗时 Generic < Humanoid   
Humanoid更省内存

### Apply Root Motion

增加CPU计算量，不建议开启。如果要开启，建议勾上optimize gameobject。

### AnimationBlend

指的是混合树，多层动画，动画状态过渡三个方面。   
会增加ProcessAnimations的开销   
避免频繁blend   
替换不必要的blend tree和layers

### Bake Mesh

将Skinned Mesh转换为普通的Mesh，运行时从网格中获取对应的网格数据进行渲染。   
缺点：需要记录Mesh信息，占用大量内存。

### GPU Skinning

用GPU计算网格，   
优点：   
减少SkinnedMesh.Render的CPU耗时   
骨骼结点信息通过纹理来存储，数据量较Bake Mesh会大幅降低   
缺点：   
增加GPU消耗，   
要求DIrectX 11或者Opengl ES 3.0

### 简化骨骼名字

unity的动画数据存储的时候按每个骨骼节点的轨道拆分存储的，每个骨骼存储的是从根节点到这个骨骼节点的hierarchy路径，字符串的，骨骼多了之后这部分字符串不少。如果把所有骨骼名字都简化，这里可以省不少内存 

## Ref

<http://nfrechette.github.io/2017/01/30/anim_compression_unity5/>   
<http://www.manew.com/thread-103127-1-1.html>   
<https://blog.csdn.net/alexander_xfl/article/details/66975570>   
<https://blog.csdn.net/j756915370/article/details/79415841>   
<https://blog.uwa4d.com/archives/Loading_AnimationClip.html>   
<http://www.360doc.com/content/17/0424/15/6432946_648246543.shtml>

