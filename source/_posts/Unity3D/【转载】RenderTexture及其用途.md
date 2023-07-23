---
title: 【转载】RenderTexture及其用途
date: 2020-12-7 18-31
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

    * 转自：https://www.jianshu.com/p/fa73c0f6762d

## 什么是RenderTexture?

RenderTexture是unity定义的一种特殊的Texture类型,它是连接着一个FrameBufferObject的存在于GPU端的Texture(Server-Side Texture),从上面对RenderTexture的解释我们了解到要先知道Texture和FrameBufferObject是什么

## 从Texture到FrameBuffer

纹理是如何被渲染到屏幕上的 ,起初纹理存在硬盘(RAM)里,它被cpu解压缩(数据在cpu端它就只是二进制数据),如果想要显示它,那么数据将会被发送给(上传到,cpu和gpu之间的通信可以理解成client和server之间的通信)GPU,gpu将它放在显存(VARM)中,显存中有一块内存区域叫做RenderBuffer(渲染缓存),RenderBuffer只是数据缓存,它还不能用作Texture渲染,尽管它现在已经是一个texture了,在这里 texture等待着被渲染,当要渲染这个Texture时,会生成一个FrameBuffer(帧缓存),当这个帧缓存被添加到默认的帧缓存物体上(FrameBufferObject)时,它就会被绘制到屏幕上.FrameBuffer指向的是显存中RenderBuffer的地址,简单的来说,RenderBuffer需要附加在FrameBuffer上,它才能是五颜六色的图片,否则它只是显存上的一堆数据,

## FrameBufferObject

FrameBufferObject是一个集合,集合了FrameBuffer,通过快速刷新Framebuffer实现动态效果,最典型的FBO就是Unity的Main Camera,它是默认的FBO,是gpu里渲染结果的目的地.但是现代gpu通常可以创建很多其他的FBO(Unity中可以创建多个Camera)，这些FBO不连接窗口区域，这种我们创建的FBO的存在目的就是允许我们将渲染结果保存在gpu的一块存储区域，待之后使用,这种用法叫做离屏渲染，这是一个非常有用的东西。Camera 输出的FBO,可以嵌在另一个FBO中,Unity中使用RenderTexture来接收FBO(可视化FBO),Game窗口是一个特殊的RenderTexture,它允许多个FBO叠加渲染,当Camera的RenderTarget都设置为null时表示输出到game窗口(没有摄像机的RenderTaget为null会显示没有摄像机进行渲染),设置不为null表示输出到某个RT.

## 如何使用FrameBufferObject?

1.将这个FBO上的结果传回CPU这边的贴图，在gles中的实现一般是ReadPixels（）这样的函数，这个函数是将当前设为可读的FBO拷贝到cpu这边的一个存储buffer，没错如果当前设为可读的FBO是那个默认FBO，那这个函数就是在截屏，如果是你自己创建的FBO，那就把刚刚绘制到上面的结果从gpu存储拿回内存。

  2. 将这个FBO上的结果拷贝到一个gpu上的texture，在gles中的实现一般是CopyTexImage2D（），它一般是将可读的FBO的一部分拷贝到存在于gpu上的一个texture对象中，直接考到server-sider就意味着可以马上被gpu渲染使用

3.将这个fbo直接关联一个gpu上的texture对象，这样就等于在绘制时就直接绘制到这个texure上，这样也省去了拷贝时间，gles中一般是使用FramebufferTexture2D（）这样的接口。

## unity是如何使用FBO的?

Unity通过上面说的第三个方法将FBO输出到RenderTexture,在unity里要使用这个FBO,只能基于这个RenderTexture(目前我知道的是这样,可能有我不知道的用法).

在Unity固定渲染管线中(Unity2019.3以后 自定义渲染管线脱离预览版,新的通用渲染管线Camera设置发生了改变,如果依然使用固定渲染管线则以下通用),通过Camera组件来使用FBO,多摄像机使用下,根据ClearFlags来决定渲染内容:

需要强调的是Clear操作, 多Camera下,DepthOnly 和Don’t Clear实际上都使Clear操作失效了 ,

## RenderTexture的用途?

1.屏幕后处理,3d游戏最基本的后处理是抗锯齿,从Unity的FrameDebugger(可以看到所有FrameBuffer,不管它们属于哪个FBO)中可以看到抗锯齿的操作在OverlayUI之前,所以各位做2d游戏的可以选择把抗锯齿关掉,其他的后处理如bloom,HDR等都是操作屏幕这个默认的RenderTexture,配合上相关效果的Material 

2.在Scene中直接将RT作为Texture传给其他材质球,操作是调用Material.SetTexture 为该RT,即可实现在另一个表面渲染另一个Camera的内容.可以制作后视镜功能

3.copy回cpu端的内存:基本操作是在当前帧渲染完毕后(协程中, yield return new WaitForEndOfFrame()),设置RenderTexture.active为目标RenderTexture(因为当前帧已渲染过,所以该RenderTexture不会被渲染).Texture.ReadPixels保存到显存.Texture.GetRawTextureData()读回cpu内存,可以保存到硬盘或者通过互联网通信(在unity中实现的截屏,录屏,实时共享屏幕).

以上2,3都属于离屏渲染的应用.

## 转自：<https://www.jianshu.com/p/fa73c0f6762d>

