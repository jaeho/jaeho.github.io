---
title: "Kotlin - Extensions"
date: 2018-08-15 18:16:00 +0900
categories: kotlin
---

What is kotlin "Extensions"?
-

Kotlin에서 제공하는 공식문서에는 [extensions](https://kotlinlang.org/docs/reference/extensions.html)을 다음과 같이 설명하고 있다.

> Kotlin, similar to C# and Gosu, provides the ability to extend a class with new functionality without having to inherit from the class or use any type of design pattern such as Decorator. This is done via special declarations called extensions. Kotlin supports extension functions and extension properties.

의미를 더듬더듬 해석해보면 다음과 같다.

> C# 과 Gosu와 유사하게 코틀린은 클래스를 상속 받거나 Decorator같은 유형의 디자인 패턴을 사용하지 않고도 새로운 기능으로 클래스를 확장할 수 있는 기능을 제공합니다. 이건 Extensions이라고 부르는 특별한 선언으로 이뤄집니다. 코틀린은 확장함수와 확장 프로퍼티를 지원합니다.

즉 `Activity`를 상속받지 않고도 `Activity`에 부가적인 함수와 프로퍼티를 추가할 수 있다는 의미이다. 잘 사용하면 `BaseActivity`나 `BaseFragment` 또는 너무 많아 혼란스럽던 `Utils`들을 정리하는데도 유용할것 같다.

특히나 주로 사용하는 코틀린의 `let()`, `run()`, `apply()`, `use()` 등 유용한 함수들은 이 Extensions으로 구현되어있기때문에 Extensions이야 말로 `Kotlin`을 시작하면 가장 먼저 알고 넘어가야할 개념이라고 생각한다.

확장 함수 만들기
-
확장 함수를 만들기 위해서는 하나만 기억하면 된다.

> 리시버를 메서드 이름의 앞에 적고 . 으로 구분한다.

위 사항을 기억하고 다음 함수를 확장함수로 변환해 보자.

```java
public class Utils {
    public static int getScreenWidth(Context context) {
        WindowManager display = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
        Point point = new Point();
        display.getDefaultDisplay().getSize(point);
        return point.x;
    }
}

```
자바 전형적인 Util클래스의 모습이다. `Context`를 전달받아 `WindoManager`를 통해 화면 사이즈를 구해 반환하는 함수이다. 이 함수를 `Context`의 확장함수로 변환하면 아래와 같다.

```kotlin
fun Context?.getScreenWidth(): Int {
    (this?.getSystemService(Context.WINDOW_SERVICE) as WindowManager).let {
        val point = Point()
        it.defaultDisplay.getSize(point)
        return point.x
    }
}
```

`Utils`클래스로 선언된 자바 함수는 사용시 

```
 Utils.getScreenWidth(context);
```
위와 같이 사용하게 되지만 `Context`를 확장한 함수의 경우 `Activity`나 `Application`등 `Context`를 확장한 클래스에서 `this.` 으로 사용할 수 있다. 물론 `this`는 생략 가능하다.

```
this.getScreenWidth()
```

