---
title: UE 移动设备调试
date: 2023-2-8 17-12
categories:
- Unreal
tags:
- Unreal
catalog: true
---

<https://www.youtube.com/watch?v=hEtu-ciPc7g>

adb logcat

Android Studio 是发现最优的源码级别调试方式

![](assets/UE%20移动设备调试/Image.png)

常用调试方法：

#define PRINT(String) {if (GEngine){GEngine->AddOnScreenDebugMessage(-1,10.0f,FColor::Red,*(String));}}

GEngine->AddOnScreenDebugMessage(-1, 5.0f, FColor::Red,

TEXT("Log by GEngine.AddOnScreenDebugMessage"));

GEngine->AddOnScreenDebugMessage(-1, 10.0f, FColor::Red, FString::Printf(TEXT("Server not connected yet.")));

<https://blog.csdn.net/m0_51819222/article/details/122511585>

<https://blog.csdn.net/Jason6620/article/details/128404026>

