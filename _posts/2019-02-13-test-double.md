---
title: "Test Double"
date: 2019-02-13 08:03:00 +0900
categories: android
classes: wide
ref: https://medium.com/@SlackBeck/%EB%8B%A8%EC%9C%84-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%BC%80%EC%9D%B4%EC%8A%A4%EC%99%80-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EB%8D%94%EB%B8%94-test-double-2b88cccd6a96

---

Test Double
-

[실용주의 프로그래머](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9788966261031&orderClick=LAH&Kc=) 저자 데이비드 토머스와 앤드류 헌트는 ```실용주의 프로그래머를 위한 단위 테스트 with JUnit```란 저서에서 이상적인 단위 테스트 작성을 위하여 필요한 Independent에 대해 이렇게 정의하고 있습니다.

>
테스트는 깔끔함과 단정함을 유지해야 한다. 즉, 확실히 한 대상에 집중한 상태여야 하며, 환경과 다른 개발자들에게서 독립적인 상태를 유지해야 한다.
>
또한 독립적이라는 것은 어떤 테스트도 다른 테스트에 의존하지 않는다는 것을 의미한다. 어느 순서로든, 어떤 개별 테스트라도 실행해 볼 수 있어야 한다. 처음 것을 실행할 때 그 밖의 다른 테스트에 의존해야 하는 상황을 원하지는 않을 것이다.
모든 테스트는 섬이어야 한다.
>
출처 : [실용주의 프로그래머를 위한 단위 테스트 with JUnit](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9788991268036&orderClick=LAH&Kc=)

이렇게 단위와 단위사이 격리를 위해 테스트 대상이 되는 단위에서 사용하는 다른 단위를 대체하기 위해 사용하는 것을 ```테스트 더블``` 이라고 한다. 테스트 더블에는 Test Stub, Mock Object, Fake Object, Test Spy, Dummy Object가 포함된다. 

> 테스트 더블은 영화 촬영시 스턴트 배역을 맡은 배우를 Double 이라 부르는데서 유례했습니다.

* Fake Object

Fake Object는 실제의 객체가 너무 느리거나 네트워크를 통해 무언가 수행해야할 경우 이를 대체하기 위해 간단한 구현체로 대체하는 것을 의미합니다.

	* 장점
		+ 다양한 시나리오에 사용할 수 있는 거의 완전한 구현을 제공합니다.
	* 단점
		+ 만들기가 어렵습니다. 
		+ 그 자체에 대한 단위 테스트가 필요할 정도로 복잡할 수 있습니다 

* Dummy Object

단순히 인스턴스화될 수 있는 수준으로만 객체를 작성하고 사용합니다. 인스턴스화된 객체가 필요할 뿐 해당 객체의 기능까지는 필요하지 않은 경우에 사용합니다.

	* 장점
		+ 만들기가 매우 쉽습니다.
	* 단점
		+ 용도가 제한적입니다.

* Test Spy

테스트에 사용되는 객체, 메소드의 사용 여부 및 정상 호출 여부를 기록하고 요청시 알려줍니다. 보통은 Mock 프레임 워크에서 기본적으로 기능을 제공합니다.

	* 장점
		+ 멤버가 올바르게 호출되었는지 확인할 수 있습니다.
	* 단점
		+ 유연성에 제약이 있습니다. 
		+ 단위 테스트에서 결과를 명확하게 제공하지 않습니다.
		
* Test Stub

> Stub 의 사전적 의미는 토막이나 동물의 짧은 꼬리를 의미한다. 

Stub은 로직이 없이 미리 정해진 원하는 값(canned answers)을 반환합니다. 테스트 상황에서 무조건 정해진 값을 반환해야 할 경우 사용할 수 있습니다. 위키피디아에 따르면 대개에 경우 호출자를 위한 "행복한 시나리오"에 예상되는 값을 작성합니다.

	* 장점: 만들기가 쉽습니다.
	* 단점
		+ 유연성에 제약이 있습니다. 
		+ 단위 테스트에서 결과를 명확하게 제공하지 않습니다. 
		+ 멤버가 올바르게 호출되었는지 여부를 확인하는 기능이 없습니다. 

* Mock Object

Martin Fowler의 [The Difference Between Mocks and Stubs](https://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs) 에서 Mock을 아래와 같이 정의하고 있습니다.

> Mocks are what we are talking about here: objects pre-programmed with expectations which form a specification of the calls they are expected to receive.

Mock은 수신할 것으로 예상되는 호출들을 예측하여 작성된 객체라는 의미인데 말 그대로 '어떤 함수가 호출 될 것이다' 라는 행위에 대한 예상을 가지고 있습니다. Stub이 값에 대한 테스트를 위한 것이라면 Mock은 단위 사이에 행위(Interaction)을 테스트하기 위해 사용한다고 보면 될 것 같습니다. 주로 상태 변경에 대한 식별이 어렵거나 반환 값으로 테스트 결과를 확인 할 수 없을 경우 유용합니다. 

	* 장점 
		+ Test Double을 효율적으로 만들 수 있습니다. 
		+ 익히기가 어렵습니다.
	* 단점
		+ 진입 장벽이 있습니다. 
		+ 단위 테스트에서 결과를 명확하게 제공하지 않습니다. 
		+ 멤버가 올바르게 호출되었는지 여부를 확인하는 기능이 없습니다. 


Reference
-
- [Mock을 이용한 단위 테스트] (http://egloos.zum.com/kingori/v/4169398)
- [The Difference Between Mocks and Stubs] (https://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs)
- [테스트 더블의 종류와 차이점] (http://www.jpstory.net/2013/07/26/know-your-test-doubles/)
- [Mock] (http://www.incodom.kr/Mock#h_c60b09ca8733be67208fc003404ecc79)


