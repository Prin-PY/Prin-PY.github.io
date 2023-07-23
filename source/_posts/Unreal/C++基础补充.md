---
title: C++基础补充
date: 2022-3-18 0-36
categories:
- Unreal
tags:
- Unreal
catalog: true
---

## cpp编译

<https://blog.csdn.net/leonliu06/article/details/78229534>

## Template

```csharp 

#include <iostream>

#include <string>

using namespace std; 

template <class T1,class T2>

class Pair 

{ 

public: 

T1 key; //关键字

T2 value; //值

Pair(T1 k,T2 v):key(k),value(v) { }; 

bool operator < (const Pair<T1,T2> & p) const; 

}; 

template<class T1,class T2>

bool Pair<T1,T2>::operator < (const Pair<T1,T2> & p) const

//Pair的成员函数 operator <

{ //"小"的意思就是关键字小

return key < p.key; 

} 

int main()

{ 

Pair<string,int> student("Tom",19); //实例化出一个类 Pair<string,int>

cout << student.key << " " << student.value; 

return 0; 

} 

``` ```csharp 

#include <iostream>

using namespace std; 

template <class T>

class A 

{ 

public: 

template <class T2>

void Func(T2 t) { cout << t; } //成员函数模板

}; 

int main()

{ 

A<int> a; 

a.Func<int>(123); //成员函数模板Func被实例化

a.Func<string>(" hello"); 

return 0; 

} 

``` 

