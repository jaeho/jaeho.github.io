---
title: "Kotlin - let() with()"
date: 2018-08-15 16:35:00 +0900
categories: kotlin
---

let()
-
- Calls the specified function block with ```this``` value as its ```argument``` and returns its ```result```.

```
public inline fun <T, R> T.let(f: (T) -> R): R = f(this)
```

- 함수를 호출하는 객체를 이어지는 코드 블록의 인자 ```it``` 으로 전달하고 그 결과값을 반환합니다.
- ex) 한번 사용할 변수인 getString(res)에 상수를 선언하지 않고 ```let()```을 사용하여 간략하게 처리.
 
```kotlin
fun Context?.toast(res: Int) {
    this?.getString(res).let {
        Toast.makeText(this, it, Toast.LENGTH_SHORT).show()        
    }
}
```
	
	
	
with()
-
- Calls the specified function block with the given receiver as its receiver and returns its result. 

```
public inline fun <T, R> with(receiver: T, f: T.() -> R): R = receiver.f()
```

- ```let()```과 다르게 ```T```를 확장하지 않고 ```with```의 첫번째 파라미터(```receiver```)로 넘깁니다. 