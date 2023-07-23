---
title: Unreal C++
date: 2022-3-11 19-11
categories:
- Unreal
tags:
- Unreal
catalog: true
---

  * 概念 
  * Compiling 
    *   * 我的Q&A 

## 概念

Forward Declaration  

![](assets/Unreal%20C++/Image.png)

## Compiling

### 

https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/DevelopmentSetup/CompilingProjects/

## 我的Q&A

### Class Naming Prefix

Actor - A

Object - U  
Enums - E  
Interface - I  
Template - T  
SWidget - S  
F - else

## 关于宏定义

### C++宏定义

编译过程  

![](assets/Unreal%20C++/Image_1.png)

![](assets/Unreal%20C++/Image_2.png)
  
https://blog.csdn.net/yanggangclcsdn/article/details/49704089

每个#define行（即逻辑行）由三部分组成：

```csharp #define 宏名 替换文本 ``` 

指令 - “#”表示这是一条预处理命令，“define”为宏命令  
宏（macro） - 一般为缩略语，其名称（宏名）一般大写，而且不能有空格，遵循C变量命令规则  
替换文本”-任意常数、表达式、字符串等

包括 有参宏 和 无参宏 两种

#### 可变宏

```csharp #define PR2(X, ...) printf("Message"#X":"__VA_ARGS__) //宏定义 double msg = 10; PR2(1, "msg = %.2f\n", msg); //宏调用 //输出结果：Message1:msg = 10.00 ``` 

#### 运算符：#，##

```csharp #define SUM(a,b) printf(#a " \+ "#b" = %d\n",((a) + (b))) //宏定义，运用 # 运算符 SUM(1 \+ 2, 3 \+ 4); //宏调用 //输出结果：1 + 2 + 3 + 4 = 10 ``` ```csharp #define NAME(n) num ## n //宏定义，使用 ## 运算符 int num0 = 10; printf("num0 = %d\n", NAME(0)); //宏调用 ``` 

"##" 运算符也可以用在替换文本中，而它的作用是起到粘合的作用，即将两个语言符号组合成一个语言符号，所以又称为“ **预处理器的粘合剂（Preprocessor Glue）** ”。

#### 宏定义 vs. typedef

```csharp #define INT1 int * typedef int * INT2; INT1 a1, b1; INT2 a2, b2; b1 = &m; //... main.c:185:8: Incompatible pointer to integer conversion assigning to 'int' from 'int *'; remove & b2 = &n; // OK ``` 

宏定义只是简单的字符串代换，在预处理阶段完成。而typede不是简单的字符串代换，而是可以用来做类型说明符的重命名的，类型的别名可以具有类型定义说明的功能，在编译阶段完成的。

#### 宏定义 vs. 函数

所以在宏定义中：#define COUNT(M) M * M 中的形参不分配内存单元，所以不作类型定义。而函数 int count(int x)中形参是局部变量，会在栈区分配内存单元，所以要作类型定义，而且实参与形参之间是“值传递”。而宏只是符号代换，不存在值传递。

```csharp #define COUNT(M) M * M //定义有参宏 int x = 6; printf("COUNT = %d\n", COUNT(x + 1));// 输出结果： COUNT = 13 printf("COUNT = %d\n", COUNT(++x)); // 输出结果： COUNT = 56 //warning:... main.c:161:34: Multiple unsequenced modifications to 'x' ``` 

COUNT(++x) 被替换为 ++x * ++x，即为 7 * 8 = 56，而不是想要 7 * 7 = 49  
不要在有参宏用使用到“++”、“–”等

#### 其他技巧与细节

换行：在结尾加反斜杠，可使多行连接

宏定义必须写在函数之外，其作用域是 #define 开始，到源程序结束。

如果重复定义宏，则不同的编译器采用不同的重定义策略。

### Unreal宏定义

#### UCALSS

The UCLASS macro gives the UObject a reference to a UCLASS that describes its Unreal-based type.  
UE4有一个管理游戏对象的强大系统。UObject是这个系统中所有对象的基类。UCLASS宏用于标记这些UObject的派生类，目的是把它们告知UObject管理系统。UCLASS的宏参数可以更加具体地指定该类型的各种行为。

每个 UCLASS 保留一个称作“类默认对象（Class Default Object）”的对象，简称 CDO。

The UCLASS() macro is used to indicate that a C++ class will be part of Unreal's **Reflection system**. This is necessary for the C++ class to be recognized by the Unreal Engine editor.  
Another advantage of using UCLASS() is that you can use **Unreal Engine's memory management system** in the C++ class.

> UCLASS宏只能修饰UObject的子类。

类型说明符（Class Specifiers）  

![](assets/Unreal%20C++/Image_3.png)
  
元数据说明符（Metadata Specifiers）  

![](assets/Unreal%20C++/Image_4.png)

#### MYPROJECT_API

Specifying MYPROJECT_API is necessary if MyProject wishes to expose the UMyObject class to other modules.

#### Unreal宏编译

The compilation of an Unreal C++ project happens in two phases.

  1. In the first phase, UnrealHeaderTool (UHT) reads the C++ headers files looking for Unreal macros and generates the necessary code that will replace the macros.
  2. In the second phase, the C++ compiler compiles the resulting code.

```csharp #pragma once #include "CoreMinimal.h" #include "GameFramework/Actor.h" #include "TutoProjectCollectable.generated.h" UCLASS() class TUTOPROJECT_API ATutoProjectCollectable : public AActor { GENERATED_BODY() ``` 

For this class, UnrealHeaderTool will generate code that will be placed in the TutoProjectCollectable.generated.h file and code that will replace the GENERATED_BODY() macro.

#### 宏定义的方式

C++代码中定义

Build.cs文件和Target.cs文件中

```csharp PublicDefinitions.Add("WITH_DIRECTXMATH=1"); ``` 

在UBT代码的文件夹（`\Engine\Source\Programs\UnrealBuildTool`）中搜索Definitions.Add就可以看到编译时添加的宏定义。

#### 常用宏配置与Unreal Editor中的效果

https://blog.csdn.net/qq_29523119/article/details/85255854

## Objects & GC

https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/Objects/

内存分配与容器：https://www.cnblogs.com/kekec/p/12012537.html

### Update

### Destroy

## Memory Management & GC

**UE4 uses the reflection system to implement a garbage collection system.**

Your classes need to derive from **UObject** in order to be enabled for garbage collection.

An object will **not be garbage collected** as long as **there is a path of references from an object in the root set to the object** in question.

If no such path to the root set exists for an object, it is called **unreachable** and will be **collected (deleted)** the next time the garbage collector runs.

The engine runs the garbage collector at certain **intervals**.

> UStructs cannot be garbage collected.

### Root Set

UObject pointer stored  
in a UPROPERTY   
in a UE4 container

Actors:  
GC druing a level's shutdown  
Once spawned, you must manually call Destroy on them to remove them from the Level without ending the Level.

This is important since, as mentioned before, **actors that have had Destroy called on them are not removed until the garbage collector runs again**. You can check the **IsPendingKill** method to see if a UObject is awaiting its deletion.

RootSet操作与判断

```csharp /** * Add an object to the root set. This prevents the object and all * its descendants from being deleted during garbage collection. */ FORCEINLINE void AddToRoot() { GUObjectArray.IndexToObject(InternalIndex)->SetRootSet(); } /** Remove an object from the root set. */ FORCEINLINE void RemoveFromRoot() { GUObjectArray.IndexToObject(InternalIndex)->ClearRootSet(); } /** * Returns true if this object is explicitly rooted * * @return true if the object was explicitly added as part of the root set. */ FORCEINLINE bool IsRooted() const { return GUObjectArray.IndexToObject(InternalIndex)->IsRootSet(); } ``` 

### Non-UObject References

Normal C++ objects (not derived from UObject) can also have the ability to add a reference to an object and prevent garbage collection --- derive from **FGCObject** and override its **AddReferencedObjects** method

### 智能指针

## 常用类型

### Numeric Types

int8/uint8: 8-bit signed/unsigned integer

int16/uint16: 16-bit signed/unsigned integer

int32/uint32: 32-bit signed/unsigned integer

int64/uint64: 64-bit signed/unsigned integer

float (32-bit) and double (64-bit) types

### Strings

#### FString

FString is a mutable string, analogous to std::string.

```csharp FString MyStr = TEXT("Hello, Unreal 4!"). ``` 

#### FText

localized text ???

```csharp FText MyText = NSLOCTEXT("Game UI", "Health Warning Message", "Low Health!") ``` ```csharp // In GameUI.cpp #define LOCTEXT_NAMESPACE "Game UI" //... FText MyText = LOCTEXT("Health Warning Message", "Low Health!") //... #undef LOCTEXT_NAMESPACE // End of file ``` 

#### FName

Rather than storing the complete string many times across every object that references it, FName uses a smaller storage footprint index that maps to a given string.

  * save memory when that string is used across many objects
  * save CPU time when comparing them- UE4 can simply check their index values to see if they match

#### TCHAR

The TCHAR type is used as a way of storing characters independent of the character set being used

https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/StringHandling/CharacterEncoding/

### Containers

相关资料：v

```csharp void RemoveDeadEnemies(TSet<AEnemy*>& EnemySet){ // Start at the beginning of the set, and iterate to the end of the set for (auto EnemyIterator = EnemySet.CreateIterator(); EnemyIterator; ++EnemyIterator) { // The * operator gets the current element AEnemy* Enemy = *EnemyIterator; if (Enemy.Health == 0) { // 'RemoveCurrent' is supported by TSets and TMaps EnemyIterator.RemoveCurrent(); } } } ``` 

#### TArray - std::vector

like std::vector, offers a lot more functionality

```csharp TArray<AActor*> ActorArray = GetActorArrayFromSomewhere(); // Tells how many elements (AActors) are currently stored in ActorArray. int32 ArraySize = ActorArray.Num(); // TArrays are 0-based (the first element will be at index 0) int32 Index = 0;// Attempts to retrieve an element at the given indexAActor* FirstActor = ActorArray[Index]; // Adds a new element to the end of the arrayAActor* NewActor = GetNewActor();ActorArray.Add(NewActor); // Adds an element to the end of the array only if it is not already in the arrayActorArray.AddUnique(NewActor); // Won't change the array because NewActor was already added // Removes all instances of 'NewActor' from the arrayActorArray.Remove(NewActor); // Removes the element at the specified index// Elements above the index will be shifted down by one to fill the empty spaceActorArray.RemoveAt(Index); // More efficient version of 'RemoveAt', but does not maintain order of the elementsActorArray.RemoveAtSwap(Index); // Removes all elements in the arrayActorArray.Empty(); ``` 

#### TMap - std::map

has quick methods for finding, adding, and removing elements based on their key

#### TSet - std::set

AddUnique, Contains - **faster**

#### Cumtom TSet/TMap

you will need to provide a **hash function** that takes a const pointer or reference to your type and returns a uint32  
This return value is known as the object's **hash code** , and should uniquely identify the object.

## Ref

https://blog.csdn.net/yanggangclcsdn/article/details/49704089  
https://romeroblueprints.blogspot.com/2020/10/the-uclass-macro.html  
https://www.geek-share.com/detail/2802042559.html  
https://docs.unrealengine.com/4.27/en-US/ProgrammingAndScripting/ProgrammingWithCPP/IntroductionToCPP/
