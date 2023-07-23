---
title: Build - 踩坑
date: 2022-9-8 20-21
categories:
- Unreal
tags:
- Unreal
catalog: true
---

网络问题导致gradle打包失败 - 解析jar包时，无法下载所依赖的库

修改为国内源头的方式尝试多次失败。

使用代理的方式成功：

修改 \Engine\Build\Android\Java\gradle\gradle\wrapper\目录下的 gradle-wrapper.properties 文件，添加http、https代理即可。

## For more details on how to configure your build environment visit

# <http://www.gradle.org/docs/current/userguide/build_environment.html>

#

# Specifies the JVM arguments used for the daemon process.

# The setting is particularly useful for tweaking memory settings.

# Default value: -Xmx1024m -XX:MaxPermSize=256m

# org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

#

# When configured, Gradle will run in incubating parallel mode.

# This option should only be used with decoupled projects. More details, visit

# <http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects>

# org.gradle.parallel=true

#Sat Jan 23 16:06:06 CST 2021

#systemProp.http.proxyHost=127.0.0.1

#systemProp.http.proxyPort=1081

#systemProp.https.proxyHost=127.0.0.1

#systemProp.https.proxyPort=1081
