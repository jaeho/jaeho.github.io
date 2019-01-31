---
title: "Kotlin - Extensions"
date: 2018-08-15 18:16:00 +0900
categories: kotlin
---

Kotlin-Extensions to DSL
-

Kotlin에서 제공하는 공식문서에는 [extensions](https://kotlinlang.org/docs/reference/extensions.html)을 다음과 같이 설명하고 있다.

> Kotlin, similar to C# and Gosu, provides the ability to extend a class with new functionality without having to inherit from the class or use any type of design pattern such as Decorator. This is done via special declarations called extensions. Kotlin supports extension functions and extension properties.

의미를 더듬더듬 해석해보면 다음과 같다.

> C# 과 Gosu와 유사하게 코틀린은 클래스를 상속 받거나 Decorator같은 유형의 디자인 패턴을 사용하지 않고도 새로운 기능으로 클래스를 확장할 수 있는 기능을 제공합니다. 이건 Extensions이라고 부르는 특별한 선언으로 이뤄집니다. 코틀린은 확장함수와 확장 프로퍼티를 지원합니다.

즉 `Activity`를 상속받지 않고도 `Activity`에 부가적인 함수와 프로퍼티를 추가할 수 있다는 의미이다. 잘 사용하면 `BaseActivity`나 `BaseFragment` 또는 너무 많아 혼란스럽던 `Utils`들을 정리하는데도 유용할것 같다.

특히나 주로 사용하는 코틀린의 `let()`, `run()`, `apply()`, `use()` 등 유용한 함수들은 이 Extensions으로 구현되어있기때문에 Extensions이야 말로 `Kotlin`을 시작하면 가장 먼저 알고 넘어가야할 개념이라고 생각한다.

Extensions Function 만들기
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

Higher-Order Function에서의 Extensions
-
[Higher-Order Function](https://kotlinlang.org/docs/reference/lambdas.html)에도 `Extension`을 적용할 수 있다.

```kotlin
fun onClick(view: View?, body: () -> Unit) {
    view?.setOnClickListener { body }
}

onClick(view, { doSomething })
```

위와 같은 Higher-Order Function이 있다고 가정하자. View의 확장 함수로 사용하면 아래처럼 수정하기 위해 아래와 같이 수정할 수 있다.

```kotlin
fun View?.onClick(onClick: () -> Unit) {
    this?.setOnClickListener { onClick }
}

view.onClick { doSomething }
```

Extensions을 사용하니 그저 View에서 onClick 함수를 부르는것 만으로도 간단한 onClick 이벤트 처리가 가능해진다!

Inline?
-
`Kotlin` 문서에서는 Higher-Order Function 과 관련하여 다음과 같이 경고하고 있다.

> Using Higherer-order functions imposes certain runtime penalties: each function is an object, and it captures a closure, i.e. those variables that are accessed in the body of the function. Memory allocations (both for function objects and classes) and virtual calls introduce runtime overhead.

> 고차 함수를 사용할때 런타임 오버해드가 있을 수 있다.

그리고 이걸 해결할 방법으로 inline 키워드를 제시하고 있다. 도대체 무슨말인지 아래의 코드를 한번 살펴 보자. 위에서 만든 View 클래스의 확장 함수 onClick을 사용한 코드이다.

```
fun TextView?.toText(msg: () -> CharSequence) {
    this?.text = msg()
}


fun multipleSetText(v1: TextView, v2: TextView, v3: TextView) {
    v1.toText { "a" }
    v2.toText { "b" }
    v3.toText { "c" }
}
```

위 코드를 Decompile하면 아래와 같은 내용이 나온다.

```
public final void multipleSetText(@NotNull TextView v1, @NotNull TextView v2, @NotNull TextView v3) {
  Intrinsics.checkParameterIsNotNull(v1, "v1");
  Intrinsics.checkParameterIsNotNull(v2, "v2");
  Intrinsics.checkParameterIsNotNull(v3, "v3");
  ExtensionsKt.toText(v1, (Function0)null.INSTANCE);
  ExtensionsKt.toText(v2, (Function0)null.INSTANCE);
  ExtensionsKt.toText(v3, (Function0)null.INSTANCE);
}
```
`toText` 함수를 사용할때마다 `Function` 객체가 생성되는 것을 확인 할 수 있다. 문서에서 지적하고 있는 오버해드가 발생하는 부분이다. 이때 inline 키워드를 적용한다면 함수 호출시 `Function`객체를 생성하지 않고 해당 함수 내용을 풀어서 써준다. 그 결과는 다음과 같다.


```
// inline 키워드 추가 
inline fun TextView?.toText(msg: () -> CharSequence) {
    this?.text = msg()
}

// Decompile 결과 
public final void multipleSetText(@NotNull TextView v1, @NotNull TextView v2, @NotNull TextView v3) {
  Intrinsics.checkParameterIsNotNull(v1, "v1");
  Intrinsics.checkParameterIsNotNull(v2, "v2");
  Intrinsics.checkParameterIsNotNull(v3, "v3");
  String var8 = "a";
  v1.setText((CharSequence)var8);
  var8 = "b";
  v2.setText((CharSequence)var8);
  var8 = "c";
  v3.setText((CharSequence)var8);
}
```

고차 함수 호출시 마다 생성되던 Function0 객체 대신 해당 `Function` 결과를 풀어써 있는것을 확인 할 수 있다. 이로써 오버해드 걱정 끝.


DSL(Domain-Specific Language)
-
위에서 살펴본 `Kotlin Extensions` 와 `Higher-Order Function`을 사용하면 간단한 DSL 형태를 만들어 사용하는 것도 가능하다. 자주쓰는 `Toast` 함수를 `Context`의 확장 함수로 적용하여 다음과 같이 쓸 수도 있다.

```
inline infix fun Context.toast(message: String) {
    Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
}

c toast "Goobye!"
```


Android Kotlin에서 많이 사용되는 DSL 

- [kotlin-anko](https://github.com/Kotlin/anko)
- [android-anko-with-kotlin (realm)](https://academy.realm.io/kr/posts/android-anko-with-kotlin/)