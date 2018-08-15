---
title: "Kotlin - let() appy() run() with() also()"
date: 2018-08-15 16:35:00 +0900
categories: kotlin
---

- let()
 - Calls the specified function block with ```this``` value as its ```argument``` and returns its ```result```.
	
 - 함수를 호출하는 객체를 이어지는 코드 블록의 인자 ```it``` 으로 전달하고 필요에따라 결과값을 반환합니다.

 - 아래와 같이 한번 사용할 변수인 getString(res)에 상수를 선언하지 않고 ```let()```을 사용하여 간략하게 처리.
 
```kotlin
fun Context?.toast(res: Int) {
    this?.getString(res).let {
        Toast.makeText(this, it, Toast.LENGTH_SHORT).show()        
    }
}
```
	
	
- apply()

- run()
- with()
- also()