---
title: Audio
date: 2020-10-9 21-26
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---

## Overview

### Basic Theory

To simulate the effects of position, Unity requires sounds to originate from Audio Sources   
attached to objects. The sounds emitted are then picked up by an Audio Listener   
attached to another object, most often the main camera. Unity can then simulate the effects of a source’s distance and position from the listener object and play them to the user accordingly. The relative speed of the source and listener objects can also be used to simulate the **Doppler Effect(多普勒效应)** for added realism.

#### 回声和混响

Unity can’t calculate echoes purely from scene geometry but you can simulate them by adding Audio Filters to objects. For example, you could apply the Echo filter to a sound that is supposed to be coming from inside a cave. In situations where objects can move in and out of a place with a strong echo, you can add a Reverb Zone to the scene. 

## Assets

Unity supports **mono** , **stereo** and **multichannel** audio assets (up to eight channels).   
Unity3D游戏引擎一共支持4个音乐格式的文件   
.AIFF 适用于较短的音乐文件可用作游戏打斗音效   
.WAV 适用于较短的音乐文件可用作游戏打斗音效   
.MP3 适用于较长的音乐文件可用作游戏背景音乐   
.OGG 适用于较长的音乐文件可用作游戏背景音乐

> Unity also supports tracker modules, which use short audio samples as “instruments” that are then arranged to play tunes. Tracker modules can be imported from .xm, .mod, .it, and .s3m files but are otherwise used in much the same way as ordinary audio clips.

## Recording

Unity can access the computer’s microphones from a script and create Audio Clips by direct recording. The **Microphone** class provides a straightforward API to find available microphones, query their capabilities and start and end a recording session.

# Clip

### Load Type

#### Decompress On Load

Use this option for smaller compressed sounds to avoid the performance overhead of decompressing on the fly. Be aware that decompressing Vorbis-encoded sounds on load will use about **ten times** more memory than keeping them compressed (for ADPCM encoding it’s about 3.5 times), so don’t use this option for large files.

适用于 **较小** 的压缩声音，避免即时解压缩的性能开销。不要使用于大文件。

#### Compressed In Memory

Keep sounds compressed in memory and decompress while playing. This option has a slight **performance overhead** (especially for Ogg/Vorbis compressed files) so only use it for bigger files where decompression on load would use a prohibitive amount of memory.   
播放时解压会有CPU开销（尤其是OGG / Vorbis格式的压缩文件），但可以提高加载速度并减少内存消 耗，因此这个选项适用于 **大文件** 。 

> The decompression is happening on the mixer thread and can be monitored in the “DSP CPU” section in the audio pane of the profiler window.

#### Streaming

Decode sounds on the fly. This method uses a minimal amount of memory to buffer compressed data that is **incrementally read from the disk and decoded on the fly.**

> Profiler中：“Streaming CPU” section in the audio pane of the profiler window.   
>  Streaming clips has an overload of approximately 200KB, even if none of the audio data is loaded.

直接从磁盘流音频数据。这只使用了原始声音占内存大小的很小一部分。 该方法使用最少的内存和最多的CPU，它有个很明显的缺点就是不能被引用超过一次。试着让 Audio Clip产生多个副本的时候会每个都产生数据缓冲区，如果非要这么做会产生大量的内存和cpu消耗。因此这个选择最好是给单实例的Audio Clip，如背景和环境音效。对于手游而言不要优先考虑使用这种方式。

### Compression Format

#### PCM

全称是Pulse-Code Modulation。属于脉冲调制编码，它将模拟信号转换为数字信号，实质上没有经过编码，没有进行压缩，所以在音质上是属于完全无损的原始音频。而且相较于原生的模拟信号，它的抗干扰能力更强，保真效果更好。

This option offers higher quality at the expense of larger file size and is best for very short sound effects.

#### ADPCM

Adaptive Differential Pulse Code Modulation，自适应差分脉冲编码调制。是一种基于PCM的优化压缩方式，但也属于有损压缩。   
This format is useful for sounds that contain a fair bit of noise and need to be played in large quantities, such as footsteps, impacts, weapons. The compression ratio is 3.5 times smaller than PCM, but CPU usage is much lower than the MP3/Vorbis formats which makes it the preferrable choice for the aforementioned categories of sounds.

#### Vorbis/MP3

应该叫做OGG Vorbis。类似mp3格式，但这是一种免费开发的非商业压缩格式。属于有损压缩。

The compression results in smaller files but with somewhat lower quality compared to PCM audio. The amount of compression is configurable via the Quality slider. This format is best for **medium length** sound effects and music.

### 使用建议

#### 占据大量内存的长音频

  * 使用流（Streaming）载入方式（Load Type），并且设置压缩格式（Compression Format）为Vorbis。如此设置即可使内存使用量减至最低，但相对的会占用更多CPU资源和I/O吞吐量。

  * 使用压缩并存储至内存（Compressed In Memory）载入方式，设置压缩格式为Vorbis。与第一个方案唯一的区别是，前者占据更多I/O吞吐，而此种方式占用更多内存。可以调整Quality滑块来通过降低音频质量来减小音频剪辑压缩后的尺寸。一般来说，100%的Quality值略高，我们推荐70%。注意，使用该种设置添加两个以上的音乐或环境声剪辑时会大量消耗CPU。

#### 短或中等长度的音频

  * 对于经常播放的短音频剪辑，使用载入时压缩（Decompress On Load）载入方式（Load Type），PCM或ADPCM压缩格式（Compression Format）。选择PCM时，播放无需解压，适用于短且使用频率高的音频剪辑。您也可以用ADPCM压缩格式，播放该格式需要解压缩，但解压缩ADPCM比Vorbis快很多。

  * 对于经常播放的中等长度剪辑，使用压缩并存储至内存（Compressed In Memory）和ADPCM压缩格式（Compression Format）。原始PCM的大小大概是ADPCM的3.5倍，ADPCM的解压缩算法也比Vorbis解压缩算法占用更少CPU。

  * 对于播放频率低的短音频剪辑，使用压缩并存储至内存（Compressed In Memory）和ADPCM压缩格式（Compression Format）

  * 对于播放频率低的中等长度剪辑，使用压缩并存储至内存（Compressed In Memory）和Vorbis压缩格式（Compression Format）。使用ADPCM处理该种声音效果（SFX）未免显得浪费了存储空间，况且播放的频率又很低，所以使用更多CPU资源解压缩还是可以接受的。

### Sample Rate Setting

Preserve Sample Rate: 保留采样率   
Optimize Sample Rate：此设置根据分析的最高频率内容自动优化采样率。   
Override Sample Rate：此设置允许手动覆盖采样率，因此可以有效地避免采样内容丢失。

## Ref

<https://docs.unity3d.com/Manual/AudioOverview.html>   
<https://www.xuanyusong.com/archives/550>   
<https://support.unity3d.com/hc/zh-cn/articles/208211393-%E6%B8%B8%E6%88%8F%E5%9C%A8%E6%92%AD%E6%94%BE%E5%A3%B0%E9%9F%B3%E5%8F%91%E7%94%9F%E5%8D%A1%E9%A1%BF>

