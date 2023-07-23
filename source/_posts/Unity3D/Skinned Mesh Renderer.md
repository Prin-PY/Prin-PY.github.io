---
title: Skinned Mesh Renderer
date: 2020-9-9 18-12
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Motion Vector

![Alt text](assets/Skinned%20Mesh%20Renderer/1606707414304.png)

Motion vectors provide you with a texture with two channels that calculate the positional difference objects render in camera space between this frame and the previous frame.

> In video compression, a motion vector is the key element in the motion estimation process. It is used to represent a macroblock in a picture based on the position of this macroblock (or a similar one) in another picture, called the reference picture. — Wikipedia   
>  In video editing motion vectors are used to compress video by storing the changes to an image from one frame to the next. — [webopedia](https://www.webopedia.com/TERM/M/motion_vector.html)

### 算法的关键点

In fact all of these terms refer to the process of finding corresponding points between two images or video frames. The points that correspond to each other in two views (images or frames) of a real scene or object are “usually” the same point in that scene or on that object. Before we do motion estimation, we must define our measurement of correspondence, i.e., the matching metric, which is a measurement of how similar two image points are. There is no right or wrong here; the choice of matching metric is usually related to what the final estimated motion is used for as well as the optimisation strategy in the estimation process.

### Unity中的Mesh Renderer Motion Vectors

**Motion vectors** track the per-pixel object velocity from one frame to the next in screen space. 描述当前像素下的片元，在相邻两帧之间，屏幕空间位置的差。

实现原理与兼容性 - When set, the camera renders another pass (after opaque but before Image Effects): First, a full screen pass is rendered to reconstruct screen-space motion from the camera movement, then, any moving objects have a custom **pass** to render their object-specific motion. The **buffer** uses the RenderTextureFormat.RGHalf format, so this feature only works on platforms where this format is supported.

**Velocity Buffer** \- 是一个全屏尺寸的 RenderTexture，motion vector 组成的Buffer。

#### 应用

  * Use this velocity to reconstruct previous positions.

  * Using this information you can apply specific Image Effects such as **motion blur** or **temporal anti-aliasing**.

#### skinned motion vectors

There is a cost to skinned motion vectors, though; they require twice as much memory per skinned mesh because the graphics memory on the GPU becomes double buffered (one buffer for the current frame and one buffer for the previous frame). The buffers track motion between frames; the velocity is the current frame’s position minus the last frame’s position.

#### 示例

使用Motion Vector实现相关的后处理特效:   
相机上的脚本: 

```csharp 

using UnityEngine; 

[ExecuteInEditMode] 

[RequireComponent(typeof(Camera))] 

public class DatamoshEffect : MonoBehaviour { 

public Material DMmat; //datamosh material

void Start () { 

this.GetComponent().depthTextureMode=DepthTextureMode.MotionVectors; 

//generate the motion vector texture @ '_CameraMotionVectorsTexture'

} 

private void OnRenderImage(RenderTexture src, RenderTexture dest)

{ 

Graphics.Blit(src,dest,DMmat); 

} 

} 

``` ```csharp 

sampler2D _MainTex; 

sampler2D _CameraMotionVectorsTexture; 

fixed4 frag (v2f i) : SV_Target 

{ 

fixed4 col = tex2D(_MainTex, i.uv); 

float4 mot = tex2D(_CameraMotionVectorsTexture,i.uv); 

col+=mot;//add motion vector values to the current colors

return col; 

} 

``` ```csharp 

fixed4 frag (v2f i) : SV_Target 

{ 

float4 mot = tex2D(_CameraMotionVectorsTexture,i.uv); 

//add motion vectors directly to UV position for sampling color

fixed4 col = tex2D(_MainTex, i.uv+mot.rg); 

return col; 

} 

``` 

## 原理

<https://gitee.com/xianglinlove/Avatar>   
<https://zhuanlan.zhihu.com/p/41763382>   
<https://github.com/xieliujian/UnityDemo_Avatar>   
<https://blog.uwa4d.com/archives/avartar.html>   
<https://github.com/zouchunyi/UnityAvater>

## 优秀的相关资料

在 Unity SRP 实现 Temporal Anti-aliasing: <https://zhuanlan.zhihu.com/p/138866533>

## Ref

<https://en.wikipedia.org/wiki/Motion_vector>   
<https://ompuco.wordpress.com/2018/03/29/creating-your-own-datamosh-effect/>   
<https://www.webopedia.com/TERM/M/motion_vector.html>   
<https://zhuanlan.zhihu.com/p/138866533>

