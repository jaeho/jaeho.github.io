---
title: "Kotlin - 유용한 함수들"
date: 2018-08-16 08:47:00 +0900
categories: kotlin
---

let()
-
> Calls the specified function block with `this` value as its `argument` and returns its `result`.

```
public inline fun <T, R> T.let(f: (T) -> R): R = f(this)
```

함수를 호출하는 객체를 이어지는 코드 블록의 인자 `it` 으로 전달하고 그 결과값을 반환한다.

 
```kotlin
fun Context?.toast(res: Int) {
    this?.getString(res).let {
        Toast.makeText(this, it, Toast.LENGTH_SHORT).show()        
    }
}
```

also()
-
> Calls the specified function `block` with `this` value as its argument and returns `this` value. 

```
public inline fun <T> T.also(block: (T) -> Unit): T
```

`let()`과 거의 유사하다. `let()`이 `R`을 리턴하는 반면 `also()`는 `T`를 리턴한다.

```
print(StringBuilder("abc").let {
	it.append("def")
	2
})
// 결과는 2

print(StringBuilder("abc").also {
	it.append("def")
	2
})
// 결과는 abcdef
```

		
with()
-
> Calls the specified function block with the given receiver as its receiver and returns its result. 

```
public inline fun <T, R> with(receiver: T, f: T.() -> R): R = receiver.f()
```

`let()`과 다르게 `T`를 확장하지 않고 `with`의 첫번째 파라미터(`receiver`)로 넘긴다. 

```kotlin
with(textView) {
	onClick {
		println("onClick)
	}
}
```

run()
-
> Calls the specified function block with `this` value as its `receiver` and returns its result.

```
public inline fun <T, R> T.run(f: T.() -> R): R = f()
```

`with()`와 유사하지만 리시버를 직접 넘기지 않고 확장한 `T`를 리시버로 전달 받는다. `with()`와 다르게 null-safety를 사용할 수 있다.


```kotlin
textView?.run {
	onClick {
		println("onClick)
	}
}
```

apply()
-
> Calls the specified function block with `this` value as its `receiver` and returns `this` value.

```
public inline fun <T> T.apply(f: T.() -> Unit): T { f(); return this }
```

`run()`과 유사하지만 `f`의 리턴값이 없고 `f` 실행 후 `this`를 리턴하는 점이 다르다.

```
val tv = TextView(ctx) {
	onClick {
		println("onClick)
	}
}
```

use()
-
> Executes the given `block` function on this resource and then closes it down correctly whether an exception is thrown or not.

```
public inline fun <T : Closeable?, R> T.use(block: (T) -> R): R 
``` 

`Closeable` 인터페이스가 구현된 클래스에 한해서 사용 가능하다, block 실행 후 반드시 `close()` 호출을 보장한다.

```
PrintWriter(FileOutputStream("output.txt")).use {
    it.println("hello")
}
```
