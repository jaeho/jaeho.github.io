---
title: "Android Test 2"
date: 2019-01-31 11:07:00 +0900
categories: android
classes: wide
---

해 볼 수 있는 것 2 "계측 테스트 (Instrumentation Test)"
- 
사실 따지고 보면 진짜 리얼한 테스트는 여기서 이뤄집니다. 실제 앱 또는 코드가 동작하는 조건에서 동일하게 실행되는 테스트이기 때문입니다. 따라서 이건 로컬 테스트에 비하여 까다롭고 유지보수가 어렵습니다. 저는 사실 이 계측 테스트로 진행하는 UI 테스트에 대해 굉장히 부정적인 입장이었습니다. 여러가지 이유가 있
지만 기본적으로 들이는 노력에 비해 얻을 수 있는게 제한적이라는게 큰 이유였죠. 하지만 잘 이용한다면 유용하게 쓰일 방법을 찾을 수 있지 않을까 그런 기대를 갖고 살펴봤습니다. 아직 답은 잘 모르겠네요. 계측 테스트에 대해 [공식 문서](https://developer.android.com/studio/test/?hl=ko)에서는 이렇게 설명합니다.

```
하드웨어 기기나 에뮬레이터에서 실행되는 테스트입니다. 
이 테스트에서는 Instrumentation API에 액세스할 수 있으며, 
테스트하는 앱의 Context 와 같은 정보에 대한 액세스 권한을 개발자에게 제공하고, 
개발자는 테스트 코드에서 테스트되는 앱을 제어할 수 있습니다. 
사용자 상호작용을 자동화하는 통합 및 기능적 UI 테스트를 작성하거나 테스트에 모의 객체가 충족할 수 없는 Android 종속성이 있는 경우 이 테스트를 사용합니다.

계측 테스트는 APK(앱 APK와는 별개임)로 빌드되므로 자체 AndroidManifest.xml 파일을 가져야 합니다. 
하지만, Gradle이 빌드 과정에서 이 파일을 자동으로 생성하므로 프로젝트 소스 세트에는 표시되지 않습니다.
`minSdkVersion`에 다른 값을 지정하거나 테스트 전용 실행 리스너를 등록하는 등과 같이 필요한 경우 자체 매니페스트 파일을 추가할 수 있습니다. 
앱을 빌드하면 Gradle이 여러 매니페스트 파일을 하나의 매니페스트 파일로 병합합니다.
```

사실 계측 테스트는 로컬 테스트와는 전혀 다른 방향으로 진행됩니다. 안드로이드에서는 주로 자동화된 UI테스트를 위해 사용한다고 알고 있습니다. 따라서 이번에는 Activity Instrumentation Test를 진행해 보겠습니다.

- Step 1. dependecies 설정

```
dependencies {
	// Core library
    androidTestImplementation 'androidx.test:core:1.0.0'
    // AndroidJUnitRunner and JUnit Rules
    androidTestImplementation 'androidx.test:runner:1.1.0'
    androidTestImplementation 'androidx.test:rules:1.1.0'
    // Assertions
    androidTestImplementation 'androidx.test.ext:junit:1.0.0'
    androidTestImplementation 'androidx.test.ext:truth:1.0.0'
    androidTestImplementation 'com.google.truth:truth:0.42'

    // Espresso dependencies
    // Contains core and basic View matchers, actions, and assertions. See Basics and Recipes.
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.1.0', {
        exclude group: 'com.android.support', module: 'support-annotations'
    }
    // External contributions that contain DatePicker, RecyclerView and Drawer actions, accessibility checks, and CountingIdlingResource.
    androidTestImplementation 'androidx.test.espresso:espresso-contrib:3.1.0'
    // Extension to validate and stub intents for hermetic testing.
    androidTestImplementation 'androidx.test.espresso:espresso-intents:3.1.0'
    androidTestImplementation 'androidx.test.espresso:espresso-accessibility:3.1.0'
    //Contains resources for WebView support.
    androidTestImplementation 'androidx.test.espresso:espresso-web:3.1.0'
    androidTestImplementation 'androidx.test.espresso.idling:idling-concurrent:3.1.0'
    //
    androidTestImplementation 'androidx.test.espresso:espresso-idling-resource:3.1.0'

    // for using uiautomator
    androidTestImplementation 'androidx.test.uiautomator:uiautomator:2.2.0'

    // for multidex
    androidTestImplementation 'com.android.support:multidex-instrumentation:1.0.2'
}
```
