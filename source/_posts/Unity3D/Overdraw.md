---
title: Overdraw
date: 2020-6-15 17-30
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## 是什么

overdraw表示一个像素的重新绘制次数，在像素处理中，overdraw是最常见的性能瓶颈之一。   
Scene视图的RenderMode->Overdraw。越亮的区域表示overdraw的程度越高，也就越消耗GPU。

> 当然这里的视图只是提供了查看物体遮挡的层数关系，并不是真正的最终屏幕绘制的overdraw。也就是说，可以理解为它显示的是如果没有使用任何深度检验时的overdraw。这种视图是通过把所有对象都渲染成一个透明的轮廓，通过查看透明颜色的累计程度，来判断物体的遮挡。

## 优化点

  * 控制绘制顺序:PC上资源无限，一般都是从后往前绘制，但在移动上，尽量从前往后绘制.在Unity中，那些Shader中被设置为“Geometry”队列的对象总是从前往后绘制的，而其他固定队列（如“Transparent”“Overla”等）的物体，则都是从后往前绘制的。这意味这，我们可以尽量把物体的队列设置为“Geometry” 。尽量减小过度绘制区域:实在需要多层绘制的地方，要尽量减小各部分过度绘制区域，使重合区域小，绘制的像素点也就少一点

  * 注意性能与效果的取舍:UGUI的许多控件有很好的通用性和展示效果，但是可能会耗更多性能

  * 过大的不必要绘制尽量代码实现:例如点击屏幕空白区域返回功能，加透明image会增加很多

  * UI设计上尽可能简单减少重叠

### 针对性优化

#### 文字

Outline实现方式是将Text的四个顶点传过去复制四份，设置四份偏移量实现效果，将偏移量设置很大之后，可以看到一个Text周围有四个相同的Text   
解决方案:   
1.不使用或者使用Shadow(Shadow通过为图像或者文字的Mesh添加顶点实现阴影效果，Outline继承Shadow，在对象四个角上各添加一个Shadow)   
2.使用Textmesh Pro(Unity5.5)需要制作相应的字体文件，对于动态生成的文字效果不好，固定字体很好   
([https://blog.csdn.net/dark00800/article/details/73011343?utm_source=itdadao&utm_medium=referral](https://blog.csdn.net/dark00800/article/details/73011343?utm_source=itdadao&utm_medium=referral))   
3.修改Mesh的UV坐标，提取文字原始UV坐标，扩大文字绘图区域，对文字纹理周围像素点采样，新旧颜色融合   
(<http://gad.qq.com/article/detail/29266>)

#### 适配IphoneX

适配的需要加了层背景，不是iPhoneX失活就可以

#### 背景人物mesh

裁剪小一点更好

#### Mask组件

Unity的Mask组件会增加一层Overdraw，还会多增加4个DrawCall   
解决:   
1.使用RectMask2D代替，缺点是只能用于矩形   
2.对于多边形，用MeshMask，红色为UnityMask，蓝色是MeshMask，UnityMask消耗15个DrawCall，Overdraw2次，MeshMask消耗1个DrawCall，1层OverDraw(<https://www.cnblogs.com/leoin2012/p/6822859.html>)

#### Image的slide属性

对于slide九宫格图片，可以看情况取消fill center属性，那样中心区域会不渲染，中心区域也就镂空，重合面积也会小

1)重合多的地方尽可能不重合   
2)无用的Image   
少量的panel或者单纯的空父物体身上加着image，虽然没有给图片，但是还是会渲染   
3)移动的波浪图片过大过多(修改高度，宽度)   
4)特效粒子效果优化(<http://www.u3dnotes.com/archives/807>)   
粒子效果薄弱的可以使用序列帧动画实现

部分小细节：   
1.slide九宫格图片，取消fill center，中心镂空   
2.mask尽量不用，可以用rect mask2D 代替   
3.不用UI/Effect，包括Shadow，Outline，Position As UV1   
4.不用Image的Tiled类型   
5.不用Pixel Perfect   
6.动静分离，动态的在父物体上加个Canvas   
7.尽量active，不要destroy，也不要设置Alpha=0这样还是会渲染   
8.不用BestFit(代价高，Unity会为该元素用到的所有字号生成图元保存在Altlas中，增加额外生成时间，还会使得字体对应的atlas变大)   
9.特效粒子

Ref：   
<https://www.jianshu.com/p/7167c516bd75>

