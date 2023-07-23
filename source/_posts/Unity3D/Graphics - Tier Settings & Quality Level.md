---
title: Graphics - Tier Settings & Quality Level
date: 2020-9-27 12-07
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

> 优化中经常提到，根据机型配置的高低，进行不同的设置，使用不同性能的资源，那么这个究竟如何实现的，Unity使用什么样的机制支持这件事？

## Graphics Tier Settings

通过图形API或者设备的版本确定一些 **全局的Graphics设置** 以及所加载的 **Shader脚本内容** 。从而达到目的: 

  * 兼容不同版本的图形API、显示设备

  * 根据设备的性能调整项目质量的高低，在性能上适应不同的设备。

> Use the Graphics settings (main menu: Edit > Project Settings, then select the Graphics category) to apply global settings for Graphics.

These settings allow you to make platform-specific adjustments to rendering and shader compilation, by tweaking built-in defines. 

### 常用设置项及其含义

### How is this selection done?

默认：Unity根据设备的版本或图形API自动选择。

#### Tier 1

Android - all devices that have support for OpenGL ES 2 only

iOS - all devices before iPhone 5S (not including 5S, but including 5C), iPods up to and including 5th generation, iPads up to 4th generation, iPad mini first generation

Desktops: DirectX 9, HoloLens

#### Tier 2

Android - all devices with OpenGL ES 3 support

iOS - all devices starting from iPhone 5S, iPad Air, iPad mini 2nd generation, iPod 6th generation   
AppleTV

Web

Vulkan on Android is Tier 2.

#### Tier 3

Desktops: OpenGL, Metal, DirectX 11+ , Vulkan 

for desktops is in Tier 3

### Scripting API

自定义：使用脚本在Runtime强行设置。

```csharp 

Graphics.activeTier : Rendering.GraphicsTier 

``` 

Initially this value is auto-detected from the hardware in use.   
**Changing this value affects any subsequently loaded shaders. (So you have to do that before any shaders are loaded.)**   
TierN corresponds to shader define UNITY_HARDWARE_TIERN

Runtime根据机型自定义Tier

```csharp 

deviceID = SystemInfo.deviceModel; 

if(deviceID == "iPhone10,3 " || deviceID == "iPhone10,6"){ 

// This is an iPhoneX

//now change the graphics tier to tier 3

Graphics.activeTier = GraphicsTier.Tier3 

} 

``` 

**set it once when you app starts.**

## Quality Level

设置方法：menu: Edit > Project Settings, then select the Quality category

Set the level of graphical quality it attempts to render.   
Generally speaking, quality comes at the expense of framerate and so it may be best not to aim for the highest quality on mobile devices or older hardware since it tends to have a detrimental effect on gameplay. 

有Unity默认的Levels，也可以自己添加Levels，自己命名。

### Scripting API

Runtime设置Level

```csharp 

using UnityEngine; 

public class Example : MonoBehaviour

{ 

void OnGUI()

{ 

string[] names = QualitySettings.names; 

GUILayout.BeginVertical(); 

for (int i = 0; i < names.Length; i++) 

{ 

if (GUILayout.Button(names[i])) 

{ 

QualitySettings.SetQualityLevel(i, true); 

} 

} 

GUILayout.EndVertical(); 

} 

} 

``` 

> Note that: changing the quality level can be an expensive operation if the new level has different anti-aliasing setting. It’s fine to change the level when applying in-game quality options, but if you want to dynamically adjustquality level at runtime, pass false to applyExpensiveChanges so that expensive changes are not always applied.   
>  When building a player quality levels that are not used for that platform are stripped. You should not expect a given quality setting to be at a given index. It’s best to query the available quality settings and use the returned index.

## 两者的区别

Graphics Tier Settings一般是在真机上运行时自动选择，由于涉及到Grapics API的兼容性，开发者或用户一般不自己改Tier。

Quality Level比较常用，开发者可以根据场景或设备的性能设置Level。或者以UI的形式把设置Level的接口开放给用户，让用户根据自己的情况选择游戏质量。

判断设备高低端的方法：   
不同的游戏厂商有不同的方法。

  * 粗糙一点的可能根据CPU的频率判断。

  * SystemInfo的API可以获取CPU等型号，根据型号判断等等。

## Ref

<https://forum.unity.com/threads/tiers-in-graphicsettings.485408/>

