---
title: "Android with Test"
date: 2019-01-31 11:07:00 +0900
categories: android
classes: wide
---

로컬(JVM) 단위 테스트
-

### Intro


* 위치: ```module-name/src/test/java/```
* [Developers 의 설명](https://developer.android.com/studio/test/?hl=ko)

```
컴퓨터의 로컬 JVM(Java Virtual Machine)에서 실행되는 테스트입니다. 
테스트에 Android 프레임워크 종속성이 없거나 Android 프레임워크 종속성에 대한 모의 객체를 생성할 수 있는 경우 이 테스트를 사용하면 실행 시간을 최소화할 수 있습니다.

런타임에 이 테스트는 모든 final 한정자가 삭제된, 수정된 버전의 android.jar에 대해 실행됩니다. 
여기서는 Mockito와 같이 흔히 사용되는 모의 라이브러리를 사용할 수 있습니다.
```
* 한계점: JVM에서 동작하는 만큼 Android Runtime 환경과 차이가 발생 할 수 있다. Mockito와 Robolectrics로 커버하지만 근본적으로 다른 환경이라는 걸 인지하고 비즈니스 로직을 검증하는데 사용해야 한다.


### Walkthrough

- dependencies 설정

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

- test 클래스 작성 
```module-name/src/test/java/com/ncsoft/sdk/test/Test.java```

```
@RunWith(RobolectricTestRunner.class)
public class Test {

    protected static final String APP_ID = "24623D7B-EDCC-D337-A5DB-A57AC5A83794";
    protected static final String APP_SECRET = "MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQCYc5fuo+wdG1BhcrM+TWWM93z2Zgr0pB7r7oa3LZT7krRNEkKeW4d0ErPFMEWJGrtJWFNY9NpiPnKe4J/Lfp4X40LJpWb/TlQfqDtDuz0+p6dXK8aIxzaMFjI3xL9rvrgV8kwnDgE8poeO4DTfZsUXUfSHGbuykxVFVVc0K8zwB0ZD+WHjIIRrmgTUGrRUSp8LDPMZuboUiFEkOXWWBiPDmLmpFl1+zImBJGh8YrvdyxbCd0RFS1aUurFHVhhJMvUnowNea6+mJWKuxOMPR/N0UNaw5Ue/jESxQENR6eGxL5vBabWGEUm/pj/SdEnB20FWu2kK6mO8kveguRjGb1+ZAgMBAAECggEBAJLDlZyUCpbq2LM3rP9pmz3edFrxWdKyvWH8u4xVQXv/e7xGvAOfsgM4jgBjvE2Fgo/VjEezURoLbGUvciaBusjcbEucBE/8pFflqUhHVWqgFCWDaxn6TrUGGUo/Ctk7PhVCsbVXcjFlUFNn3P7E/TC6IWJ+j4gWuP+KbO04zY60tZeanpbxVtnpomN4zrQ3lrLM6OELYehncAW+eJvieq/J0cHKljf5d63CuWc24DlLfJEu0IZ5g5s86113eyNkCTBccg9TcxGfILt7Bywb+lCyZhQjpr7r98hpzGWhtpx+5GpxTA9kPBWgeq4OvIJnGjLOPCiZrai0t1Rq69soAgECgYEAyxfNhv0W3QAOmKLiE+zL7pWfT30R9GNNEB9A1Vs8Cq6JxojgXnwkACGIKeKrwA2cRen9MpdS0Orhy3EKlUUByP6SAdgqEGHAhTg4fXIz43A3a+iyhR6iutKCJQQpxngQFMAx7iLwUmMg3Keh3Q0/33RidrsLUkaZ+jHmjuAIiEkCgYEAwCqH/EL9He/BIJp6TThSByrV51U5kq5zXDuXl4Eil1gzcf/YrAwOk+TRkHlqWLsVrw0t1BzpoWoHGEVlVOkn4u2G9SyT9vzG84aRlHEAGxDrFa0q+WlYVOSYaYRfeGiKuX3gKGBieUby4CFJ/7LKbnRzV1V6xbAyejkK20lPPNECgYEAvNm0bzq24Ohlqj+ENHz0ITYWfubRJEyWY1B8jCkbSt+EFA5BfPq4yzpjEHfLt3mwgD6WCE44Xzaaof/KlIUnpMw73uUwMC2FxRtDRDtGzs4RaxFlt22GamzHQj59ziTk5zbU9xicGjA9ZZGnbRMd+t6RlNBXNbmbAtEWEHN426kCgYEAvQdZWxE+UbttO7gZhGpZbkl5vqR8DMjkG59XICZcM4oEmSg2KA94K40ThE2bCguGafrJ0PRb8XcN4Zcp9Zugq75BWl1uc6/1uMnv3JhHpVhAF8OPGWbCCEgRkQIws44KoCqtXKprU6cx9L1qQEfMj1inuQoRyfLnxIjmIA1+D3ECgYEArdTZJdySTCFjveObNwhMzPKOed7GGsPOJvhE3qwqoQehmyNakyANZXe4qmsKzvy5xRiqxwgW0lokafysOD8Pw1IOYkv3vEXwJapSXcHuQfwh80FhG7OcRixT87GE2QslNUZ35S3JplRENUmErW3k5TPGryB4tzVfEC+FdIGESUg=";
    protected static final String SESSION = "0250305D-9732-418D-8648-19655197171B";
    protected static final String RC = "https://rc-api.ncsoft.com/";
    
    @Before
    public void setUp() throws Exception {
        Context context = Mockito.mock(Context.class);
        Nc2Sdk.initialize(context, new Nc2SessionProvider() {
            @Override
            public String getSession() {
                return SESSION;
            }

            @Override
            public void refreshSession(OnRefreshedSession onRefreshedSession) {

            }
        }, APP_ID, APP_SECRET);

        RuntimeEnvironment.APIGATE_URL = RC;
        RuntimeEnvironment.GAMEDATA_GAME_KEY = "lms";
        RuntimeEnvironment.BUCKET_HOST_URL = "https://rc-api.ncsoft.com";
    }
    
    @Test
    public void getGameUserArticleCount() throws Exception {
        Nc2Article.GameUser gameUser = Mockito.mock(Nc2Article.GameUser.class);
        gameUser.gameCharacterId = "215BADC1-4041-11E7-80CD-00155D01E804";
        gameUser.gameUserUid = "A692B5C8-103C-4390-8F23-0CB7C1DAFDF3";
        gameUser.gameServerId = 1;

        Nc2ApiResponse<Nc2User.ArticleCount> response = Nc2User.getArticleCount(gameUser);
        out.println(response);
        assertTrue(response.isSuccess());
    }
}
```

- Troubleshooting	
	- 네트워크 연결 테스트중 https 연결에 대하여 PKIX path validation failed: java.security.cert.CertPathValidatorException: Algorithm constraints check failed on signature algorithm: SHA384WithRSAEncryption 발생
	- 다음 클래스를 생성 한다. ```src/test/java/android/security/NetworkSecurityPolicy```

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

### With Jacoco


**What is Jacoco?** 자코코는 **Ja**va **Co**de **Co**verage의 줄임말이다. Android Studio는 유닛 테스트를 지원하지만 테스트 커버리지 측정은 자체적으로 지원하지 않고 있기 때문에 테스트 커버리지를 측정할 수 있는 툴이 필요하다. Java의 코드 커버리지 측정툴 중 가장 유명한것은 Cobertuna지만 Jacoco가 gradle 플러그인 지원, Java 7/8 지원, Runtime에 실행 가능한 점 등의 특성 때문에 많이 사용되고 있다.

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


계측 테스트
- 

* 위치: ```module-name/src/androidTest/java/```
* [Developers 의 설명](https://developer.android.com/studio/test/?hl=ko)

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
