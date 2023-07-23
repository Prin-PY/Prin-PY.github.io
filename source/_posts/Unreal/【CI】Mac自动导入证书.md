---
title: 【CI】Mac自动导入证书
date: 2022-2-22 22-45
categories:
- Unreal
tags:
- Unreal
catalog: true
---

```csharp pipeline { stages { stage('Code Sign') { steps { sh """ # Create Temp Keychain and Import security create-keychain -p $TEMP_KEYCHAIN_PASSWORD $TEMP_KEYCHAIN_NAME security import $CERT_FILE_PATH -k $TEMP_KEYCHAIN_NAME -P $CERT_PASSPHRASE -T /usr/bin/codesign # Set Partition List security set-key-partition-list -S apple-tool:,apple: -s -k $TEMP_KEYCHAIN_PASSWORD $TEMP_KEYCHAIN_NAME # Set Search List security list-keychains -s `security list-keychains | xargs` $TEMP_KEYCHAIN_NAME # Other Settings security set-keychain-settings -t 3600 $TEMP_KEYCHAIN_NAME security unlock-keychain -p $TEMP_KEYCHAIN_PASSWORD $TEMP_KEYCHAIN_NAME # Show Identities security find-identity -vp codesigning # Do your own work here """ } } } post { cleanup { sh """ # Remove Temp Keychain security delete-keychain $TEMP_KEYCHAIN_NAME || true """ } }} ``` 
