---
title: Mipmap与Texture Streaming
date: 2022-8-18 17-22
categories:
- Unreal
tags:
- Unreal
catalog: true
---

Texture Streaming：

<https://zhuanlan.zhihu.com/p/544892912>

<https://zhuanlan.zhihu.com/p/520393454>

<https://zhuanlan.zhihu.com/p/546756533>

<https://zhuanlan.zhihu.com/p/474701022>

Mipmap：

# 【纹理优化（三）】善用Mipmap：<https://zhuanlan.zhihu.com/p/351712352>

Mipmap会额外消耗内存

纹理大小和实际上最终图元在屏幕上显示的大小差别很大。Mipmap可以用来解决：失真、摩尔纹现象；GPU带宽过大问题；

Streaming：

只加载部分Mipmap图片以节省更多的内存及显存空间。

通过消耗少量 CPU 资源来节省潜在的大量 GPU 内存。

* * *

UE Streaming介绍：

UE 的 Texture Streaming基于纹理的mipmap技术，为了优化Texture对于内存的占用而存在。对于生成了mipmap的纹理，会根据一套规则来计算纹理资源所需要的理想的Mipmap层级，结合内存池的大小，来对纹理进行动态地流式送入、送出内存，这样就避免了纹理的所有mipmap都进内存。

