---
title: "Android Test"
date: 2019-01-31 11:07:00 +0900
categories: android
classes: wide
---

What is Test Code?
-
구글에 "test code"를 검색해보면 결과가 5,490,000,000개, 범위를 조금 좁혀 "android test code"를 검색해 보면 1,180,000,000개가 검색 됩니다. 이처럼 많은 관심을 받고 있는 테스트 코드 우리는 어디까지 알고 어디까지 활용하고 있을까요?

간단히 정의하자면 테스트 코드는 코드에 대한 검증을 위한 코드입니다. 예를 들어 살펴보겠습니다. 다음은 IU의 IUri.getHost() 함수가 제대로 동작하는지 알아보기위한 테스트 코드입니다. 아래 코드는 IUri.getHost()의 결과가 예상된 결과에 맞는지 검증하고 있습니다. 

```
@Test
public void getHostHome() {
    IUri.Host excepted = IUri.Host.Home;
    IUri.Host input = IUri.getHost(Uri.parse("nc2://home"));
    Assert.assertEquals(input, excepted);
}

@Test
public void getHostUnknown() {
    IUri.Host excepted = IUri.Host.Unknown;
    IUri.Host input = IUri.getHost(Uri.parse("nc2://whatislove"));
    Assert.assertEquals(input, excepted);
}
```

간단하게 작성된 위 테스트 코드는 어떤점에서 필요할까요?

1. 먼저 혹시 있을지 모르는 코드상의 오류를 발견할 수 있게 도와줍니다. 
2. 반복적으로 수행할 테스트를 자동화하여 편의성을 높여줍니다.
3. 설계를 개선합니다.
	- 이건 매우 중요한 항목입니다.
	- 위 코드가 제대로 동작하는것을 검증하기 위해서는 getHost() 함수가 매우 독립적으로 동작하도록 설계되어야 되는것이 우선입니다. 
	- 다른 코드를 수정했을때 위 테스트 코드의 결과가 변하게 되는 상황을 모니터링 할 수 있게 되어 설계를 수정하고 독립적인 모듈로 동작하도록 수정할수 있도록 가이드합니다.
4. 테스트 코드 자체가 하나의 가이드 역할을 합니다.
	- 추후 이 프로젝트를 넘겨받을 사람은 문서가 아닌 테스트 코드를 보고 해당 코드의 역할과 기대되는 동작을 유추할 수 있게 됩니다. 잘짜여진 테스트 코드는 인수인계 문서를 줄여줍니다.
5. 뿌듯합니다.
	- 커버리지는 어떤 절대적인 척도도 될 수 없지만 높아지는 커버리지는 개발자 가슴 깊은 곳의 만족감을 충족 시켜줍니다. (적어도 저한테는 그랬습니다)


Test In Android
-
그렇다면 우리가 사랑하는 Android에서의 테스트는 어떤가요? 불행하게도 Android는 테스트를 수행하기에 많은 장벽이 있습니다. 이게 바로 오늘 이와 같은 문서를 마련한 이유이기도 하죠. Android 테스트가 어려운 많지만 정리해보자면 다음과 같습니다.

1. Mock 객체를 사용하기 굉장히 까다로운 구조입니다.
	- Android는 기본적으로 android.test.mock 패키지를 통해 MockContext, MockApplication, MockResource와 같은 기본적인 Mock 객체를 제공합니다. 하지만 이들의 구현체는 UnsupportedOperationException만 뱉는 사용하기 어려운 껍데기입니다. 만약 필요하다면 이 Mock객체를 직접 구현해야하는데 이건 쉬운일이 아닙니다.
	
2. 테스트를 위해 제공되는 Istrumentation Test가 난해합니다.
	- ActivityTestCase, ActivityUnitTestCase, ActivityInstrumentationTestCase2 등 정체 불명의 도구들이 많습니다. 내 Application 객체의 Function 하나를 테스트 하기위해, 또는 내 Activity의 동작을 테스트하기위해 무엇을 선택해야 하는지 부터 고민스러워 집니다.
	- 참고로 ActivityUnitTestCase는 레이아웃 및 격리 된 메서드를 테스트하는 데 사용하며 ActivityInstrumentationTestCase2는 터치/마우스 이벤트를 보내고 Activity의 상태 관리를 테스트하려는 경우 사용할 수 있습니다. 일반적으로 ActivityTestCase는 사용하지 않습니다.
	
3. UI 테스트는 원래 어렵습니다.
	- 이건 비단 Android의 이슈는 아닙니다. iOS도 웹도 PC 어플리케이션도 UI 생성과 이벤트를 다루는 코드는 테스트하기 어려운 분야입니다. 
	- 그 효용성에 대해서도 갑을논박이 많은 분야입니다. UI 객체의 속성은 자주 바뀌고 익명 클래스 등을 통해 처리되는 이벤트는 Mock 객체로 바꾸고 추적하기가 어렵습니다.
	
4. 테스트는 느립니다.
	- "apk 패키징 > apk 설치 > 실행" 과정 이 선행 되어야 하기 때문에 누군가의 PC처럼 시스템 자체가 빠르지 않은 경우가 아니더라고 해도 Android의 테스트 프레임워크는 기본적인 java 테스트에 비해 느립니다. 

그럼에도 불구하고 우리는 Android Test를 100% 포기 할 수는 없습니다. 위와 같은 제약이 있다 하더라도 테스트의 의의를 살릴 수 있고 무의미한 짓이 아닌 효용성 있는 테스트 코드 작성을 위해 끊임 없이 고민해야합니다. 왜냐면 ~~저 위에서 자꾸 그걸 시키기 때문~~ 우리는 작은 코드 한줄에도 치열하게 고민하고 끊임없이 개선해 나아가야 할 운명을 갖고 사는 개발자이기 때문입니다. 그러니 해 볼 수 있는것 부터 하나씩 시작해 봅시다.


해 볼 수 있는 것 "로컬(JVM) 단위 테스트"
-

Android의 높은 진입 장벽을 우회하여 일단 UI가 아닌 비즈니스 로직부터 검증해 봅시다. 하지만 그냥 Java에서는 한없이 간단했던 이 일조차 Android 에서는 그리 녹록치 않습니다. 본래 Android Runtime에서 수행되어야 할 테스트가 PC JVM에서 실행되는 만큼 다른 환경에 따른 추가 처리가 필요하기 때문입니다. [공식 문서](https://developer.android.com/studio/test/?hl=ko)에서는 로컬 단위 테스트에 대해 아래와 같이 소개하고 있습니다.

```
컴퓨터의 로컬 JVM(Java Virtual Machine)에서 실행되는 테스트입니다. 
테스트에 Android 프레임워크 종속성이 없거나 Android 프레임워크 종속성에 대한 모의 객체를 생성할 수 있는 경우 이 테스트를 사용하면 실행 시간을 최소화할 수 있습니다.

런타임에 이 테스트는 모든 final 한정자가 삭제된 수정된 버전의 android.jar에 대해 실행됩니다. 
여기서는 Mockito[^1]와 같이 흔히 사용되는 모의 라이브러리를 사용할 수 있습니다.
```

테스트 테스크가 시작되면 중간에 ```mockableAndroidJar``` 테스크를 호출하는것을 확인 할 수 있습니다. 이 테스크가 위 소개글에서 설명하는 android.jar 파일을 mock 인터페이스 형태로 컴파일하는 테스크 입니다. 문제는 android.jar가 mock 형태의 기능을 제공하기 때문에 사실상 아무런 기능을 하지 않는다는 것입니다. 아마도 처음 테스트 코드를 작성하며 Android 프레임워크에 기능을 사용하게 되면 이런 에러 메시지를 만난 경험이 있을 것입니다. 

```
java.lang.RuntimeException: Stub!?
```

이런 부분을 해결하기 위해서는 Stub으로 구현된 부분을 실제로 구현해야 합니다만 이건 테스트를 위한 테스트 코드 작성을 요구하여 테스트의 무결성에 영향을 줄 뿐아니라 무엇보다 굉장히 번거롭습니다.

> 꼭 코드 작성이 아니라 Stub에 해당하는 라이브러리를 직접 추가해 줄 수도 있습니다. 예를들어 Android 프레임 워크에 포함된 ```org.json.JSONObject``` 객체를 사용하며 Stub!? 이 발생한 경우 JSONObject 라이브러리를 추가하여 해결 할 수도 있습니다.

이런 한계점을 개선하기 위해 시도되고 있는 여러 프로젝트중 가장 유명하고 많이 사용하는것이 ```Robolectric``` 입니다. Robolectric은 JVM에서 Android SDK가 제공하는 코드를 가로채 정상 실행 될 수 있도록 동작합니다.

Android 프레임워크에 대한 종속성을 Robolectric이 어느정도 해결해 준다고 하더라도 말그대로 로컬(JVM)에서 동작하는 만큼 Android Runtime 환경과 차이가 발생 할 수 있습니다. 로컬 테스트는 근본적으로 다른 환경이라는 걸 인지하고 비즈니스 로직을 검증하는데 사용해야 합니다.


- Step1. dependencies 설정

```
dependencies {
	// JUnit 4 framework
	testImplementation 'junit:junit:4.12'
	
	// Robolectric environment
	testImplementation 'org.robolectric:robolectric:3.5'    
	
	// Mockito framework
	testImplementation 'org.mockito:mockito-core:2.7.6'
}
```

- Step2. deafultConfig 설정에 testInstrumentationRunner 추가

```
android {
	defaultConfig {
		testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
	}
}
```

- Step3. Test 코드 작성 
	- 기본 위치: ```{module-name}/src/test/java/{package-path}/Test.java```
	- Test 클래스를 작성할때 주의점은 @RunWith 어노테이션으로 실행할 러너를 지정해줘야 하는점을 잊지 말아야 합니다. 저 같은 경우 항상 그걸 잊어서 Empty Test Suit 오류를 보고 뭘까 한번씩 꼭 생각하게 됩니다.
	- 실습해봅시다.

- Robolectics를 이용한 깨알 꿀팁
	- Logcat을 콘솔로 출력 하고 싶을때는?
		- ```ShadowLog.stream = System.out;```
	- 특정 버전의 단말에서 테스트를 실행하는 것처럼 환경을 설정하고 싶을때는?
		- ```Robolectric.Reflection.setFinalStaticField(Build.VERSION.class, "SDK_INT", Build.VERSION_CODES.JELLY_BEAN);```


Troubleshooting	
-

프로젝트에 테스트를 적용하며 발생했던 이슈에 대해 간략하게 정리해봤습니다.

- java.lang.AbstractMethodError: org.powermock.api.mockito.internal.mockmaker.PowerMockMaker.isTypeMockable(Ljava/lang/Class;)Lorg/mockito/plugins/MockMaker$TypeMockability;

	- 권장 솔루션: 아래 종속성을 추가한다.

```
	testImplementation "org.powermock:powermock-module-junit4:1.6.2"
	testImplementation "org.powermock:powermock-api-mockito:1.6.2"
```

- 네트워크 연결 테스트중 https 연결에 대하여 PKIX path validation failed: java.security.cert.CertPathValidatorException: Algorithm constraints check failed on signature algorithm: SHA384WithRSAEncryption

	- 권장 솔루션: 다음 클래스를 생성 한다. ```src/test/java/android/security/NetworkSecurityPolicy```

```
package android.security;
 
import android.annotation.SuppressLint;
 
public class NetworkSecurityPolicy {
    private static final NetworkSecurityPolicy INSTANCE = new NetworkSecurityPolicy();
 
    @SuppressLint("NewApi")
    public static NetworkSecurityPolicy getInstance() {
        return INSTANCE;
    }
 
    public boolean isCleartextTrafficPermitted() {
        return true;
    }
}
```

Jacoco
-

**What is Jacoco?** 자코코는 **Ja**va **Co**de **Co**verage의 줄임말입니다. Android Studio는 유닛 테스트를 지원하지만 테스트 커버리지 측정은 자체적으로 지원하지 않고 있기 때문에 테스트 커버리지를 측정할 수 있는 툴이 필요하죠. Java의 코드 커버리지 측정툴 중 가장 유명한것은 Cobertuna지만 Jacoco가 gradle 플러그인 지원, Java 7/8 지원, Runtime에 실행 가능한 점 등의 특성 때문에 많이 사용되고 있습니다.

- Jacoco의 적용

```
apply plugin: 'jacoco' // 빌드 스크립트에서 Jacoco 사용할 수 있도록 설정

jacoco {
    reportsDir = file("${buildDir}/reports") // 측정 결과가 저장될 경로를 지정
}

task coverageReport(type: JacocoReport, dependsOn: 'testDebugUnitTest') {
    group = "Reporting"
    description = "Generate Jacoco coverage reports"

    def coverageSourceDirs = ['src/main/java']

    classDirectories = fileTree(
            dir: "${buildDir}/intermediates/classes/debug",
            excludes: ['**/R.class',
                       '**/R$*.class',
                       '**/BuildConfig.*',
                       '**/Manifest*.*',
                       'com/android/**/*.class']
    )

    sourceDirectories = files(coverageSourceDirs)
    executionData = files("${buildDir}/jacoco/testDebugUnitTest.exec")

    reports {
        xml.enabled = true
        html.enabled = true
    }
}
```
task 상세

- dependsOn: 테스트 수행 후 커버리지 측정이 진행될 수 있도록, 유닛 테스트를 수행하는 태스크 이름으로 지정합니다. 사용하는 안드로이드 그래들 빌드 플러그인 버전에 따라 다르게 지정해야 하며, 사용 중인 플러그인 버전은 루트 프로젝트의 build.gradle에서 확인할 수 있습니다. 버전별로 지정해야 하는 이름은 다음과 같습니다.
	- 1.2.3 이하: testDebug
	- 1.3.0 이상: testDebugUnitTest
- coverageSourceDirs(sourceDirectories): 커버리지를 측정할 소스 디렉터리를 지정합니다.
- classDirectories: 소스 디렉터리 내 클래스를 컴파일한 결과인 *.class 파일이 있는 디렉터리를 지정합니다. 커버리지 측정에서 제외해야 하는 클래스(R, 안드로이드 서포트 라이브러리 등)는 제외합니다.
- executionData: 커버리지 측정 결과를 저장할 파일 이름을 지정합니다. 플러그인 버전에 따라 다르게 지정합니다.
	- 1.2.3 이하: testDebug.exec
	- 1.3.0 이상: testDebugUnitTest.exec
- reports: 커버리지 결과 리포트 형식을 지정합니다.


[^1]: Mock의 필요성