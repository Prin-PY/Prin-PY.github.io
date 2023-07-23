---
title: An introduction to IL2CPP internalsВведение в
date: 2020-6-2 23-44
categories:
- Unity3D
tags:
- Unity3D
catalog: true
---
 IL2CPP - Unity Technologies Blog

# An introduction to IL2CPP internals

[Josh Peterson](https://blogs.unity3d.com/author/josh/ "Posts by Josh Peterson"), May 6, 2015

[Technology](https://blogs.unity3d.com/category/technology/)

[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='470.5' height='470.5' viewBox='0 0 470.5 470.5' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='278' class='js-evernote-checked'%3e%3cstyle data-evernote-id='279' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3cpath d='M271.5 154.2v-40.5c0-6.1 0.3-10.8 0.8-14.1 0.6-3.3 1.9-6.6 3.9-9.9 2-3.2 5.2-5.5 9.7-6.7 4.5-1.2 10.4-1.9 17.9-1.9h40.5V0h-64.8c-37.5 0-64.4 8.9-80.8 26.7 -16.4 17.8-24.6 44-24.6 78.7v48.8h-48.5v81.1h48.5v235.3h97.4V235.3h64.8l8.6-81.1H271.5z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='280' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F)[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='450' height='450' viewBox='0 0 450 450' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='282' class='js-evernote-checked'%3e%3cstyle data-evernote-id='283' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3cpath d='M450 85.7c-17.7 7.6-35.4 12.4-53.1 14.3 20-12 33.5-28.9 40.5-50.8 -18.3 10.8-37.8 18.3-58.5 22.3 -18.3-19.4-40.7-29.1-67.4-29.1 -25.5 0-47.2 9-65.2 27 -18 18-27 39.7-27 65.2 0 6.9 0.8 13.9 2.3 21.1 -37.7-1.9-73-11.4-106.1-28.4C82.5 110.2 54.4 87.5 31.4 59.1c-8.4 14.3-12.6 29.8-12.6 46.5 0 15.8 3.7 30.5 11.1 44 7.4 13.5 17.4 24.5 30 32.8 -14.8-0.6-28.7-4.5-41.7-11.7v1.1c0 22.3 7 41.8 21 58.7 14 16.8 31.6 27.5 53 31.8 -8 2.1-16.1 3.1-24.3 3.1 -5.3 0-11.1-0.5-17.4-1.4 5.9 18.5 16.8 33.6 32.5 45.5 15.8 11.9 33.7 18 53.7 18.4 -33.5 26.3-71.7 39.4-114.5 39.4 -8.2 0-15.6-0.4-22.3-1.1 42.8 27.6 90 41.4 141.6 41.4 32.7 0 63.5-5.2 92.2-15.6 28.7-10.4 53.3-24.3 73.7-41.7 20.4-17.4 37.9-37.4 52.7-60.1 14.8-22.7 25.7-46.3 33-70.9 7.2-24.7 10.8-49.3 10.8-74.1 0-5.3-0.1-9.3-0.3-12C421.8 120.2 437.2 104.3 450 85.7z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='284' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://twitter.com/intent/tweet?url=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F&text=An+introduction+to+IL2CPP+internals&via=unity3d)[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='438.5' height='438.5' viewBox='0 0 438.5 438.5' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='286' class='js-evernote-checked'%3e%3cstyle data-evernote-id='287' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3crect x='5.4' y='145.9' width='94.2' height='282.9' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='288' class='js-evernote-checked'%3e%3c/rect%3e %3cpath d='M408.8 171.7c-19.8-21.6-46-32.4-78.5-32.4 -12 0-22.9 1.5-32.7 4.4 -9.8 3-18.1 7.1-24.8 12.4 -6.8 5.3-12.1 10.3-16.1 14.8 -3.8 4.3-7.5 9.4-11.1 15.1v-40.2h-93.9l0.3 13.7c0.2 9.1 0.3 37.3 0.3 84.5 0 47.2-0.2 108.8-0.6 184.7h93.9V270.9c0-9.7 1-17.4 3.1-23.1 4-9.7 10-17.8 18.1-24.4 8.1-6.6 18.1-9.9 30.1-9.9 16.4 0 28.4 5.7 36.1 17 7.7 11.3 11.6 27 11.6 47V428.8h93.9V266.7C438.5 225 428.6 193.3 408.8 171.7zM53.1 9.7c-15.8 0-28.6 4.6-38.4 13.8C4.9 32.8 0 44.4 0 58.5c0 13.9 4.8 25.5 14.3 34.8 9.5 9.3 22.1 14 37.7 14h0.6c16 0 28.9-4.7 38.7-14 9.8-9.3 14.6-20.9 14.4-34.8 -0.2-14.1-5-25.7-14.6-35C81.6 14.3 68.9 9.7 53.1 9.7z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='289' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F&title=An+introduction+to+IL2CPP+internals&summary=Almost+a+year+ago+now%2C+we+started+to+talk+about+the+future+of+scripting+in+Unity.+The+new+IL2CPP+scripting+backend+promised+to+bring+a+highly-performant%2C+highly-portable+virtual+machine+to+Unity.+In+January%2C+we+shipped+our+first+platform+using+IL2CPP%2C+iOS+64-bit.+The+Unity+5+release+brought+another+platform%2C+WebGL.+Thanks+to+the+input+from+%5B%26hellip%3B%5D&source=Unity3d+Blog)

Almost a year ago now, we started to talk about the [future](http://blogs.unity3d.com/2014/05/20/the-future-of-scripting-in-unity/) of scripting in Unity. The new IL2CPP scripting backend promised to bring a highly-performant, highly-portable virtual machine to Unity. In January, we shipped our first platform using IL2CPP, [iOS 64-bit](http://blogs.unity3d.com/2015/01/29/unity-4-6-2-ios-64-bit-support/). The Unity 5 release brought another platform, [WebGL](http://blogs.unity3d.com/2014/04/29/on-the-future-of-web-publishing-in-unity/). Thanks to the input from our tremendous community of users, we have shipped many patch release [updates](http://blogs.unity3d.com/2015/04/07/weekly-ios-64-bit-and-metal-update/) for IL2CPP, steadily improving its compiler and runtime.

We have no plans to stop improving IL2CPP, but we thought it might be a good idea to take a step back and tell you a little bit about how IL2CPP works from the inside out. Over the next few months, we’re planning to write about the following topics (and maybe others) in this IL2CPP Internals series of posts:

  1. The basics – toolchain and command line arguments (this post)
  2. [A tour of generated code](http://blogs.unity3d.com/2015/05/13/il2cpp-internals-a-tour-of-generated-code/)
  3. [Debugging tips for generated code](http://blogs.unity3d.com/2015/05/20/il2cpp-internals-debugging-tips-for-generated-code/)
  4. [Method calls](http://blogs.unity3d.com/2015/06/03/il2cpp-internals-method-calls/) (normal methods, virtual methods, etc.)
  5. [Generic sharing implementation](http://blogs.unity3d.com/2015/06/16/il2cpp-internals-generic-sharing-implementation)
  6. [P/invoke wrappers for types and methods](http://blogs.unity3d.com/2015/07/02/il2cpp-internals-pinvoke-wrappers/)
  7. [Garbage collection integration](http://blogs.unity3d.com/2015/07/09/il2cpp-internals-garbage-collector-integration/)
  8. [Testing frameworks and usage](http://blogs.unity3d.com/2015/07/20/il2cpp-internals-testing-frameworks/)

In order to make this series of posts possible, we’re going to discuss some details about the IL2CPP implementation that will surely change in the future. Hopefully we can still provide some useful and interesting information.

**What is IL2CPP?**

The technology that we refer to as IL2CPP has two distinct parts.

  * •An ahead-of-time (AOT) compiler
  * •A runtime library to support the virtual machine

The AOT compiler translates Intermediate Language (IL), the low-level output from .NET compilers, to C++ source code. The runtime library provides services and abstractions like a garbage collector, platform-independent access to threads and files, and implementations of internal calls (native code which modifies managed data structures directly).

**The AOT compiler**

The IL2CPP AOT compiler is named il2cpp.exe. On Windows you can find it in the Editor\Data\il2cpp directory. On OSX it is in the Contents/Frameworks/il2cpp/build directory in the Unity installation. The il2cpp.exe utility is a managed executable, written entirely in C#. We compile it with both .NET and Mono compilers during our development of IL2CPP.

The il2cpp.exe utility accepts managed assemblies compiled with the Mono compiler that ships with Unity and generates C++ code which we pass on to a platform-specific C++ compiler.

You can think about the IL2CPP toolchain like this:

[
![](assets/An%20introduction%20to%20IL2CPP%20internalsВведение%20в/il2cpp-toolchain-smaller.png)
](https://blogs.unity3d.com/wp-content/uploads/2015/04/il2cpp-toolchain-smaller.png)

**The runtime library**

The other part of the IL2CPP technology is a runtime library to support the virtual machine. We have implemented this library using almost entirely C++ code (it has a little bit of platform-specific assembly code, but let’s keep that between the two of us). We call the runtime library libil2cpp, and it is shipped as a static library linked into the player executable. One of the key benefits of the IL2CPP technology is this simple and portable runtime library.

You can find some clues about how the libil2cpp code is organized by looking at the header files for libil2cpp we ship with Unity (you’ll find them in the Editor\Data\PlaybackEngines\webglsupport\BuildTools\Libraries\libil2cpp\include directory on Windows, or the Contents/Frameworks/il2cpp/libil2cpp directory on OSX). For example, the interface between the C++ code generated by il2cpp.exe and the libil2cpp runtime is located in the codegen/il2cpp-codegen.h header file.

One key part of the runtime is the garbage collector. We’re shipping Unity 5 with [libgc](https://github.com/ivmai/bdwgc/), the Boehm-Demers-Weiser garbage collector. However, libil2cpp has been designed to allow us to use other garbage collectors. For example, we are researching an integration of the Microsoft GC which was open-sourced as part of the CoreCLR. We’ll have more to say about this in our post about garbage collector integration later in the series.

**How is il2cpp.exe executed?**

Let’s take a look at an example. I’ll be using Unity 5.0.1 on Windows, and I’ll start with a new, empty project. So that we have at least one user script to convert, I’ll add this simple MonoBehaviour component to the Main Camera game object:

1

2

3

4

5

6

7

| 

using UnityEngine;

public class HelloWorld : MonoBehaviour {

void Start () {

Debug.Log("Hello, IL2CPP!");

}

}  
  
---|---  
  
When I build for the WebGL platform, I can use [Process Explorer](https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx) to see the command line Unity used to run il2cpp.exe:

1

| 

"C:\Program Files\Unity\Editor\Data\MonoBleedingEdge\bin\mono.exe" "C:\Program Files\Unity\Editor\Data\il2cpp/il2cpp.exe" \--copy-level=None \--enable-generic-sharing \--enable-unity-event-support \--output-format=Compact \--extra-types.file="C:\Program Files\Unity\Editor\Data\il2cpp\il2cpp_default_extra_types.txt" "C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\Managed\Assembly-CSharp.dll" "C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\Managed\UnityEngine.UI.dll" "C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\il2cppOutput"  
  
---|---  
  
That command line is pretty long and horrible, so let’s unpack it. First, Unity is running this executable:

1

| 

"C:\Program Files\Unity\Editor\Data\MonoBleedingEdge\bin\mono.exe"  
  
---|---  
  
The next argument on the command line is the il2cpp.exe utility itself.

1

| 

"C:\Program Files\Unity\Editor\Data\il2cpp/il2cpp.exe"  
  
---|---  
  
The remaining command line arguments are passed to il2cpp.exe, not mono.exe. Let’s look at them. First, Unity passes five flags to il2cpp.exe:

  * •–copy-level=None 
    * Specify that il2cpp.exe should not perform an special file copies of the generated C++ code.
  * •–enable-generic-sharing 
    * This is a code and binary size reduction feature. IL2CPP will share the implementation of generic methods when it can.
  * •–enable-unity-event-support 
    * Special support to ensure that code for Unity events, which are accessed via reflection, is correctly generated.
  * •–output-format=Compact 
    * Generate C++ code in a format that requires fewer characters for type and method names. This code is difficult to debug, since the names in the IL code are not preserved, but it often compiles faster, since there is less code for the C++ compiler to parse.
  * •–extra-types.file=”C:\Program Files\Unity\Editor\Data\il2cpp\il2cpp_default_extra_types.txt” 
    * Use the default (and empty) extra types file. This file can be added in a Unity project to let il2cpp.exe know which generic or array types will be created at runtime, but are not present in the IL code.

It is important to note that these command line arguments can and will be changed in later releases. We’re not at a point yet where we have a stable and supported set of command line arguments for il2cpp.exe.

Finally, we have a list of two files and one directory on the command line:

  * •“C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\Managed\Assembly-CSharp.dll”
  * •“C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\Managed\UnityEngine.UI.dll”
  * •“C:\Users\Josh Peterson\Documents\IL2CPP Blog Example\Temp\StagingArea\Data\il2cppOutput”

The il2cpp.exe utility accepts a list of all of the IL assemblies it should convert. In this case they are the assembly containing my simple MonoBehaviour, Assembly-CSharp.dll, and the GUI assembly, UnityEngine.UI.dll. Note that there are a few conspicuously missing assembles here. Clearly, my script references UnityEngine.dll, and that references at least mscorlib.dll, and maybe other assemblies. Where are they? Actually, il2cpp.exe resolves those assemblies internally. They can be mentioned on the command line, but they are not necessary. Unity only needs to mention the root assemblies (those which are not referenced by any other assembly) explicitly.

The last argument on the il2cpp.exe command line is the directory where the output C++ files should be created. If you are curious, have a look at the generated files in that directory, they will be the subject of the next post in this series. Before you do though, you might want to choose the “Development Player” option in the WebGL build settings. That will remove the –output-format=Compact command line argument and give you better type and method names in the generated C++ code.

Try changing various options in the WebGL or iOS Player Settings. You should be able to see different command line options passed to il2cpp.exe to enable different code generation steps. For example, changing the “Enable Exceptions” setting in the WebGL Player Settings to a value of “Full” adds the –emit-null-checks, –enable-stacktrace, and –enable-array-bounds-check arguments to the il2cpp.exe command line.

**What does IL2CPP not do?**

I’d like to point out one of the challenges that we did not take on with IL2CPP, and we could not be happier that we ignored it. We did not attempt to re-write the C# standard library with IL2CPP. When you build a Unity project which uses the IL2CPP scripting backend, all of the C# standard library code in mscorlib.dll, System.dll, etc. is the exact same code used for the Mono scripting backend.

We rely on C# standard library code that is already well-known by users and well-tested in Unity projects. So when we investigate a bug related to IL2CPP, we can be fairly confident that the bug is in either the AOT compiler or the runtime library, and nowhere else.

**How we develop, test, and ship IL2CPP**

Since the initial public release of IL2CPP at version 4.6.1p5 in January, we’ve shipped 6 full releases and 7 patch releases (across versions 4.6 and 5.0 of Unity). We have corrected more than 100 bugs mentioned in the release notes.

In order to make this continuous improvement happen, we develop against only one version of the IL2CPP code internally, which sits on the bleeding edge of the trunk branch in Unity used to ship alpha and beta releases. Just before each release, we port the IL2CPP changes to the specific release branch, run our tests, and verify all of the bugs we fixed are corrected in that version. Our QA and Sustained Engineering teams have done incredible work to make delivery at this rate possible. This means that our users are never more than about one week away from the latest fixes for IL2CPP bugs.

Our user community has proven invaluable by submitting many high quality bug reports. We appreciate all the feedback from our users to help continually improve IL2CPP, and we look forward to more of it.

The development team working on IL2CPP has a strong test-first mentality. We often employee Test Driven Design practices, and seldom merge a pull request without good tests. This strategy works well for a technology like IL2CPP, where we have clear inputs and outputs. It means that the vast majority of the bugs we see are not unexpected behavior, but rather unexpected cases (e.g. it is possible to use an 64-bit IntPtr as a 32-bit array index, causing clang to fail with a C++ compiler error, and [real code](http://forum.unity3d.com/threads/4-6-3-il2cpp-xcode-build-errors.299561/) actually does this!). That difference allows us to fix bugs quickly with a high degree of confidence.

With the help of our community, we’re working hard to make IL2CPP as stable and fast as possible. By the way, if any of this excites you, [we’re hiring](http://unity3d.com/jobs/position?id=oWfh0fwc) (just sayin’).

**More to come**

I fear that I’ve spent too much time here teasing future blog posts. We have a lot to say, and it simply won’t all fit in one post. Next time, we’ll dig into the code generated by il2cpp.exe to see how your project actually looks to the C++ compiler.

[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='470.5' height='470.5' viewBox='0 0 470.5 470.5' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='599' class='js-evernote-checked'%3e%3cstyle data-evernote-id='600' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3cpath d='M271.5 154.2v-40.5c0-6.1 0.3-10.8 0.8-14.1 0.6-3.3 1.9-6.6 3.9-9.9 2-3.2 5.2-5.5 9.7-6.7 4.5-1.2 10.4-1.9 17.9-1.9h40.5V0h-64.8c-37.5 0-64.4 8.9-80.8 26.7 -16.4 17.8-24.6 44-24.6 78.7v48.8h-48.5v81.1h48.5v235.3h97.4V235.3h64.8l8.6-81.1H271.5z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='601' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F)[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='450' height='450' viewBox='0 0 450 450' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='603' class='js-evernote-checked'%3e%3cstyle data-evernote-id='604' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3cpath d='M450 85.7c-17.7 7.6-35.4 12.4-53.1 14.3 20-12 33.5-28.9 40.5-50.8 -18.3 10.8-37.8 18.3-58.5 22.3 -18.3-19.4-40.7-29.1-67.4-29.1 -25.5 0-47.2 9-65.2 27 -18 18-27 39.7-27 65.2 0 6.9 0.8 13.9 2.3 21.1 -37.7-1.9-73-11.4-106.1-28.4C82.5 110.2 54.4 87.5 31.4 59.1c-8.4 14.3-12.6 29.8-12.6 46.5 0 15.8 3.7 30.5 11.1 44 7.4 13.5 17.4 24.5 30 32.8 -14.8-0.6-28.7-4.5-41.7-11.7v1.1c0 22.3 7 41.8 21 58.7 14 16.8 31.6 27.5 53 31.8 -8 2.1-16.1 3.1-24.3 3.1 -5.3 0-11.1-0.5-17.4-1.4 5.9 18.5 16.8 33.6 32.5 45.5 15.8 11.9 33.7 18 53.7 18.4 -33.5 26.3-71.7 39.4-114.5 39.4 -8.2 0-15.6-0.4-22.3-1.1 42.8 27.6 90 41.4 141.6 41.4 32.7 0 63.5-5.2 92.2-15.6 28.7-10.4 53.3-24.3 73.7-41.7 20.4-17.4 37.9-37.4 52.7-60.1 14.8-22.7 25.7-46.3 33-70.9 7.2-24.7 10.8-49.3 10.8-74.1 0-5.3-0.1-9.3-0.3-12C421.8 120.2 437.2 104.3 450 85.7z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='605' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://twitter.com/intent/tweet?url=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F&text=An+introduction+to+IL2CPP+internals&via=unity3d)[ 
![](data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' version='1.1' x='0' y='0' width='438.5' height='438.5' viewBox='0 0 438.5 438.5' xml:space='preserve' fill='rgb\(0%2c 0%2c 0\)
' data-evernote-id='607' class='js-evernote-checked'%3e%3cstyle data-evernote-id='608' class='js-evernote-checked'%3e.s0 %7b fill: rgb\(0%2c 0%2c 0\)%3b %7d%3c/style%3e %3crect x='5.4' y='145.9' width='94.2' height='282.9' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='609' class='js-evernote-checked'%3e%3c/rect%3e %3cpath d='M408.8 171.7c-19.8-21.6-46-32.4-78.5-32.4 -12 0-22.9 1.5-32.7 4.4 -9.8 3-18.1 7.1-24.8 12.4 -6.8 5.3-12.1 10.3-16.1 14.8 -3.8 4.3-7.5 9.4-11.1 15.1v-40.2h-93.9l0.3 13.7c0.2 9.1 0.3 37.3 0.3 84.5 0 47.2-0.2 108.8-0.6 184.7h93.9V270.9c0-9.7 1-17.4 3.1-23.1 4-9.7 10-17.8 18.1-24.4 8.1-6.6 18.1-9.9 30.1-9.9 16.4 0 28.4 5.7 36.1 17 7.7 11.3 11.6 27 11.6 47V428.8h93.9V266.7C438.5 225 428.6 193.3 408.8 171.7zM53.1 9.7c-15.8 0-28.6 4.6-38.4 13.8C4.9 32.8 0 44.4 0 58.5c0 13.9 4.8 25.5 14.3 34.8 9.5 9.3 22.1 14 37.7 14h0.6c16 0 28.9-4.7 38.7-14 9.8-9.3 14.6-20.9 14.4-34.8 -0.2-14.1-5-25.7-14.6-35C81.6 14.3 68.9 9.7 53.1 9.7z' fill='rgb\(0%2c 0%2c 0\)' data-evernote-id='610' class='js-evernote-checked'%3e%3c/path%3e%3c/svg%3e) ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fblogs.unity3d.com%2F2015%2F05%2F06%2Fan-introduction-to-ilcpp-internals%2F&title=An+introduction+to+IL2CPP+internals&summary=Almost+a+year+ago+now%2C+we+started+to+talk+about+the+future+of+scripting+in+Unity.+The+new+IL2CPP+scripting+backend+promised+to+bring+a+highly-performant%2C+highly-portable+virtual+machine+to+Unity.+In+January%2C+we+shipped+our+first+platform+using+IL2CPP%2C+iOS+64-bit.+The+Unity+5+release+brought+another+platform%2C+WebGL.+Thanks+to+the+input+from+%5B%26hellip%3B%5D&source=Unity3d+Blog)
