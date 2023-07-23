---
title: Unity中Culling相关技术
date: 2021-4-23 21-40
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Frustum Culling

剔除被其他物体遮挡的，摄像机不可见(但在视锥体内)的渲染物体。使用 Occlusion Culling 需要手动设置，并在 Occlusion Culling Window 中通过 Bake 计算剔除数据。   
<https://docs.unity3d.com/Manual/OcclusionCulling.html>

### Builtin管线

视锥体剔除 - 视锥体剔除是引擎自己做的，在给GPU提交数据进行渲染前，会执行视锥体剔除，决定哪些可见哪些不可见。经过剔除之后，Renderer的isVisible值就表示相应物体的可见性，不过此时已经在这帧的Update之后了。在Update当中取IsVisible属性获取的实际上是上一帧的可见性。 至于视锥体剔除的实现方法我们不清楚，可能引擎底层会有一些优化，使用kd-tree进行空间划分等等。

### SRP的Culling

  1. SRP的Culling可以自己写

  2. URP的管线相对比较固定，可定制化程度低，Culling不太好自己写

Occlusion Culling is different from Frustum Culling. Frustum Culling only disables the renderers for objects that are outside the camera’s viewing area but does not disable anything hidden from view by overdraw. Note that when you use Occlusion Culling you will still benefit from Frustum Culling.

## Occlusion Culling

在移动端使用的比较少，属于用 CPU时间换一定的CPU时间和一定的GPU时间的操作。使用方法是：预先烘焙遮挡剔除信息（对于一定的区域，哪些物体被遮挡），在游戏运行时，经过视锥体剔除之后，对于视锥体内的物体，相机到了一定的位置，会去取预先烘焙的信息，来判断哪些物体被遮挡，对相应的物体进行剔除，进而节省被遮挡的物体提交渲染进行、在GPU端进行绘制的时间。

## Camera.layerCullDistance

For performance reasons, you might want to cull small objects earlier. For example, small rocks and debris could be made invisible at much smaller distance than large buildings. To do that, put small objects into a separate layer and set up per-layer cull distances using Camera.layerCullDistances script function.   
<https://docs.unity3d.com/ScriptReference/Camera-layerCullDistances.html>

## CullingGroup API

CullingGroup offers a way to integrate your own systems into Unity’s culling and LOD pipeline.The CullingGroup will calculate visibility based on frustum culling and static occlusion culling only. It will not take dynamic objects into account as potential occluders.   
<https://docs.unity3d.com/Manual/CullingGroupAPI.html>

Unity的CullingGroup API是纯逻辑的东西，不影响渲染。其使用方法是：在逻辑代码中定义CullingGroup，Group中加入一些球体(位置与半径，是逻辑上的球体，实际是不可见的)，并加入要检测的相机，渲染时，Unity会判断这些球体是否可见，进而判断CullingGroup的可见性。在渲染之后，可以在代码中获取该Group的可见性，进而据此控制一些逻辑。如果不用代码去取CullingGroup的信息，那么它就是没有用的。

## ref

<https://blog.csdn.net/kenight/article/details/82760667>

