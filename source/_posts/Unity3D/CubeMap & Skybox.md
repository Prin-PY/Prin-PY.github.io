---
title: CubeMap & Skybox
date: 2021-3-8 11-46
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Cubemap

A Cubemap is a collection of **six square textures** that represent the reflections on an environment. The six squares form the faces of an imaginary cube that surrounds an object; each face represents the view along the directions of the world axes (up, down, left, right, forward and back).

可以使用方向向量对它们索引和采样

```csharp 

samplerCUBE _CubeMap; 

fixed4 frag (v2f i) : SV_Target 

{ 

fixed4 col = texCUBE(_CubeMap, normalize(i.vertexLocal.xyz)); 

return col; 

} 

``` 

## 制作方法

### Legacy Cubemap Assets

![Alt text](assets/CubeMap%20&%20Skybox/1615185104728.png)

### Cubemap texture

![Alt text](assets/CubeMap%20&%20Skybox/1615185140709.png)

### PanoramaToCubemap

![Alt text](assets/CubeMap%20&%20Skybox/1615185709526.png)

### Shader实现

使用Texture2D格式，在Shader当中组织，而不使用Unity的Cubemap格式。

![Alt text](assets/CubeMap%20&%20Skybox/1615185174675.png)

## Skybox的实现

### 使用Cubemap

制作Cubemap资源 。Buitin Shader当中的Skybox/Cubemap可以对Cubemap采样

![Alt text](assets/CubeMap%20&%20Skybox/1615185387170.png)

### 在Shader中对6张图采样

Builtin Shader: Mobile-Skybox

![Alt text](assets/CubeMap%20&%20Skybox/1615185458141.png)

### Panorama(全景画)

Builtin Shader: Skybox/Panoramic   
可以直接Texture2D格式的对全景图进行采样。

# Ref

<https://blog.csdn.net/v_xchen_v/article/details/79474193>

