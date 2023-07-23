---
title: GPU和CPU的区别
date: 2020-4-23 23-43
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

### GPU

GPU比较适合大量可并行的简单任务。比如场景渲染，光照处理等等。  
GPU也支持一些其他的运算，比如通过GLSL，HLSL和Cg支持并行运算等等。  
GPU同时也对游戏中的一些物理效果提供支持，比如PhysX。  
**GPU负责显示特效**

### CPU

CPU用于一些数值运算，比如伤害，随机数等等。同时你的敌人AI也是CPU运算出来的。  
越是大型的单机游戏，游戏资源量越大，资源的实时加载以及处理也是大多由CPU来完成的。  
**CPU负责游戏逻辑**
