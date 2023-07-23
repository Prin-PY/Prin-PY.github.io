---
title: Image & Raw Image
date: 2020-9-9 11-51
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Image

### 特点

而Image提供了四种ImageType：Simple（普通）、Sliced（切割）、Tiled（平铺）、Filled（填充），而且它还是布局元素（ILayoutElement），可以被各种布局组（ILayoutGroup）所包含，将它和其他布局元素进行布局。

### 属性

Source Image：只支持Sprite类型的图片   
Color：给图片混合上颜色   
Material：材质(一些特殊情况需要使用材质)   
Raycast Target：是否接收射线检测   
Image Type：图片类型(普通，九宫切图，平铺，填充)   
Preserve Aspect：是否保持宽高比   
Set Native Size：设置元素为原本的像素大小

#### Image Type

##### Simple

随意拉伸，会变形，可以勾选上PreserveAspect按原宽高比进行拉伸

##### Sliced

按照Sprite Editor中的九宫格进行拉伸处理

![Alt text](assets/Image%20&%20Raw%20Image/20200103131209912.png)
   
1，3，7，9区域不会进行拉伸，2和8区域会横向拉伸，4和6区域会纵向拉伸，5区域横纵都会拉伸

##### Tilled

图片本身大小会保持不变，像铺地面砖那样填充满整个Image控件

![Alt text](assets/Image%20&%20Raw%20Image/20200103132414236.png)

##### Filled

图片以不同的方式呈现出来，例如技能冷却，血条，进度条

## Raw Image

> the Image control requires its Texture to be a Sprite   
>  the Raw Image can accept any Texture.

### 特点

raw: 生的，未加工的   
支持任何一种贴图模式，包括Render Texture和Movie Texture   
只为我们提供了修改UV的方法，除此之外都是继承自MaskableGraphic的方法

> DefaultTexture类型会将贴图宽和高转换为2的n次幂   
>  Sprite类型不会对宽和高进行自动拉伸，可以在Inspector—Advanced—Non—Power of 2选择是否进行转换

### 属性

Color   
Material   
Raycast Target   
UV Rect：设置UV缩放和偏移(x和y属性用于控制UV左右、上下偏移，W和H属性用于控制UV的重复次数)

> 可以在Import Settings中的Wrap Model设置循环的模式，Repeat模式可以用于2D游戏的背景图循环

Set Native Size：设置元素为原本的像素大小

## Ref

<https://blog.csdn.net/ecidevilin/article/details/52556724>   
[/article/details/103807887?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.channel_param”>https://blog.csdn.net/LLLLL/article/details/103807887?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.channel_param](http://"https://blog.csdn.net/LLLLL<strong)

