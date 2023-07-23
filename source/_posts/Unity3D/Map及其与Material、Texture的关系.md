---
title: Map及其与Material、Texture的关系
date: 2020-6-8 14-38
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Map

> 贴图的英语 Map 其实包含了另一层含义就是“映射”。   
>  贴图指的是映射关系，其功能就是把纹理通过 UV 坐标映射到3D 物体表面。贴图包含了除了纹理以外其他很多信息，比方说 UV 坐标、贴图输入输出控制等等。

UV坐标：水平方向是U，竖直方向是V。因为图片（纹理）是一个二维的平面，所以只需要UV坐标便可以确定图片的位置。（当然也有三维贴图，要用到UVW坐标，暂时还接触不到。）

## 三者关系

材质 Material包含贴图 Map，贴图包含纹理 Texture。   
材质(Material)：物体的质地，物体看起来是什么做的   
贴图(Map)   
纹理(Texture)：普通的材质图片   
贴图 + 着色器(Shader) = 材质球

## Ref

<https://gameinstitute.qq.com/community/detail/115074>

