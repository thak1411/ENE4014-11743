# Rn's programming language course finalterm note

Rn's programming language course finalterm note

i wrote this note for my finalterm exam. core keywords and concepts are included in this note.

# Table of contents

- \[8주\] Subprogram
- \[9주\] Implementing Subprogram
- \[9주\] Implementing Subprogram (2)
- \[10주\] Abstract Data Types and Encapsulation Constructs (1)
- \[10주\] Abstract Data Types and Encapsulation Constructs (2)
- \[12-12주\] OOP_concurrency
- \[12주\] Concurrency
- \[12-13주\] Concurrency_exception_event
- \[13주\] Exception_event_FPL
- \[14주\] FPL (1)
- \[14주\] FPL (2)

---

# \[8주\] Subprogram

## Fundamentals of subprograms

일반적인 특성

* Single entry point (시작점 하나)
* One subprogram in execution (하나만 실행 됨)
* Control return to the caller after termination (종료 후 호출자로 제어 반환)
* Most subprogram has names (대부분의 서브프로그램은 이름을 가짐) C#은 어나니머스함
* coroutines와 concurrent에서 양자택일

### Basic definitions

* interface와 actions을 설명하는 것으로 정의 가능하다.
* subprogram은 call 당한 시점 이후로 active하다.
* subprogram은 procedure와 function으로 나뉜다.

서브 프로그램은 다음 정보를 (Header) 포함한다.

1. 이름
2. 매개변수 (parameter)
3. 실행문 (body conatins actions)

* **protocol** of subprogram: 파라미터 정보 + 반환 타입 (parameter profile + return type)
* **declarations**은 protocol of subprogram을 제공하지만, 실행문 (body)는 포함하지 않는다.
  * declarations은 static type checking이 필요하다.

### Parameters

파라미터는 두 가지 방식으로 접근 (access) 가능하다.

1. 비지역 (전역, non-local) 변수에 직접 접근 - 너무 많은 곳에 접근하면 신뢰성 (reliabilty)가 떨어진다.
2. 파라미터 전달 (parameter passing) - 더 유연하다. (more flexible)

비지역 변수를 변경하거나 클래스 변수를 변경한다면 (즉 함수 외부 변수) 다음 문제가 생길 수 있다.

1. 부작용 (side effect)가 발생할 수 있다. 부작용은 피해야 한다.
2. 신뢰성 문제가 생길 수 있다.

함수형 언어(Functional Language)에서는 변경 가능한 (Mutable) 데이터가 없다. 따라서 문제가 발생할 수 없다.


파라미터는 다음 정보로 구분 가능하다.

* Formal parameter: subprogram의 선언부 (헤더) 나타나는 파라미터 (정의)
* Actual parameter: subprogram을 호출할 때 전달하는 파라미터 (실제 값)
* Position parameter: Actual parameter를 Formal parameter에 전달 (Binding)할 때 위치에 의해 결정되는 파라미터
* Keyword parameter: Actual parameter를 Formal parameter에 전달할 때 이름에 의해 결정되는 파라미터
* Default value: Actual parameter를 생략할 때 사용되는 값 (정의)
* Absent actual parameter: Actual parameter가 생략해서 호출 (사용)

C++에는 keyword parameter가 없기 떄문에, Default value는 중간에 올 수 없다. Python의 경우 중간에 default value가 있을 수 있다. (여기서 중간은 파라미터 중간)

```python
def compute_pay(income, exemptions = 1, tax_rate):
    body...

compute_pay(20000.0, tax_rate = 0.15)
```

### Subprogram are Collection of Statements <- ?? / Procedure & Funtion

Subprogram은 크게 두 가지로 나뉠 수 있다.

1. Procedures:
    * return value가 없다.
    * variable을 변경할 수 있다. (procedure 안에서 볼 수 있는 모든 변수, 비지역 포함)
    * Formal parameter가 caller에게 데이터를 전달하는 것을 허용한다. (쉽게 바꾸면 out-mode 혹은 레퍼런스가 가능하다.)
2. Functions:
    * return value가 있다.
    * 수학적 함수를 기반으로 설계됐다.
    * 이상적인 함수라면, 부작용 (side effect)이 전혀 없다.
    * 연산자로도 정의될 수 있다. (operator overloading)

## Design Issues for subprograms

1. parameter-passing methods를 하나 이상 골라야 한다.
2. Type checking은 어떻게 할 것인가?
3. Static or dynamic local variables를 사용할 것인가.
4. Nested subprograms를 허용할 것인가?
5. subprogram을 parameter로 passing할 수 있게 할 것인가. (일급 객체로 만들 것인가)
6. subprogram이 nested된 상태로 parameter passing됐을 때 referencing environment (해당 함수가 접근할 수 있는 스코프의 단계) 를 어떻게 처리할 것인가.
7. overloaded or generic subprograms를 허용할 것인가.
8. closure를 허용할 것인가.

## Local Referencing Environments

### local variable

local variable은 두 가지 방식으로 생성할 수 있다.

1. Static: 전역변수처럼 할당되지만, subprogram 내에서만 접근 가능한 변수다.
2. Stack-Dynamic: subprogram이 실행될 때 할당되고, 종료될 때 해제되는 변수 우리가 일번적으로 아는 지역 변수다.
    * 이 방식을 사용하면 전역 recursive call을 할 수 있다.
    * active subprogram일 경우 공유될 수 있다.
    * allocation, initialization, deallocation에 시간이 든다.
    * 스택에 할당되는 변수를 간접적으로 접근해야 한다. ([esp + 8] 같은 식) 반면, Static 방식이면 0x40404040 처럼 접근 가능
    * 함수가 종료되면 지역 변수를 더이상 사용할 수 없다.

### Global variable

* subprogram 밖에 정의된다.
* declaring 없이 사용할 수 있다.
* 전역변수 이름을 함수 내에서 사용하면, 지역 변수가 우선시 된다. 따라서 의도치 않은 버그를 방지해준다.

### Nested subprogram

* 논리적인 계층 구조를 만든다.
* only needed in another subprogam일때만 사용된다. (아마 내부적으로 특정 subprogram에서만 사용되는 경우를 뜻하는 듯.)
* 다른 subprogram에서 사용하지 못 하도록 가릴때 사요ㅇ된다.

## Parameter Passing Methods

### Semantics model (formal parameter)

* in mode: 데이터를 받기 위해서 사용된다 (변경 불가)
* out mode: 데이터를 넘겨주기 위해서 사용된다. (읽기 불가)
* in-out mode: 데이터를 받고 넘겨주기 위해서 사용된다. (읽기 쓰기 가능)

### Implementation Models

* Pass-by-value: actual parameter의 값을 복사해서 전달한다.
    * in mode에서 사용된다.
    * copy를 이용해서 구현된다.
    * 복사해서 전달하는 이유는 원본 변수를 보호하기 위해서이다.
    * scalars(크기가 작은 데이터 등)에 대해서는 효율적이다.
    * 추가적인 storage가 필요하다.
    * 크기가 큰 데이터일 경우 복사에 많은 시간이 필요하다.
* Pass-by-result: actual parameter의 값을 변경해서 전달한다.
    * out mode에서 사용된다.
    * 함수에게 전달되는 데이터는 없다.
    * 함수가 종료되면 actual parameter에 값을 넘겨준다.
    * copy를 이용해서 구현된다. (반환할 때)
    * actual parameter의 초기 값을 사용(읽기)하지 않도록 주의해야 한다.

다음 경우 구현에 따라 다른 결과가 나올 수 있다.

```c
void fixer(out int x, out int y) {
    x = 17;
    y = 18;
}
fixer(out a, out a);
```

또한, call 시점에 전달받을 actual parameter를 결정할 지, return 시점에 결정할 지에 따라 결과가 달라진다.

```c++
void Dolt(out int x, out int y) {
    y = 5;
    x = 17;
}
int sub = 3;
int[] list = new int[6]{4, 0, 1, 0, 21, 12};
Dolt(out list[sub], out sub);
```

* Pass-by-value-result: actual parameter의 값을 복사해서 전달하고, 함수가 종료되면 actual parameter에 값을 넘겨준다.
    * in-out mode에서 사용된다.
    * pass-by-value + pass-by-result이다.
    * pass-by-copy라고도 불린다.
* Pass-by-reference: actual parameter의 주소를 전달한다.
    * in-out mode에서 사용된다. (하지만 pass-by-value-result와 조금 다르다.)
    * actual parameter의 주소를 전달한다.
    * 원본 변수가 변경될 수 있다.
    * copy가 없기 때문에 효율적이다.
    * indirect addressing(pointer dereferencing)이 필요해서 느리다.
    * 의도치 않은 결과를 만들 수 있다.
    * 별칭을 만들 수 있기에 신뢰성이 떨어진다.
* Pass-by-name: 어떤 값을 넘겨주냐에 따라 복사해서 전달하거나, 주소를 전달한다.
    * 변수를 넘겨줄 경우 pass-by-reference처럼 동작한다.
    * 상수를 넘겨줄 경우 pass-by-value처럼 동작한다.
    * 구현하기 어렵고 비효율적이다.

## Implementing Parameter Passing Methods

Runtime Stack을 활용해서 파라미터를 전송한다.

## Design Considerations for Parameter Passing Methods

* Efficiency: 효율적인 방법을 선택해야 한다.
* Minimize access to data outside subprogram: subprogram 외부 데이터에 접근을 최소화해야 한다.
* Minimize functional side effect: 부작용을 최소화해야 한다.

## Parameter That are Subprograms

subprogram을 parameter로 넘겨줄 수도 있다. (함수가 일급 객체일 경우)

이때 발생하는 문제는 두 가지다.

* Type checking function's protocol: 타입 체킹 시 함수의 프로토콜을 체크해야 한다.
* Function would be nested: 함수가 중첩될 수 있다. 이때 referencing environment (접근 가능 변수 스코프) 를 어떻게 처리할 것인가.

nested subprogram을 parameter로 넘겨줄 때 referencing environment를 결정하기 위한 세 가지 방법이 있다.

* Shallow binding: 실제 함수가 실행되는 위치에서 static하게 스코프를 결정한다 (코드 상에서 실행하는 위치 상으로 상위 블록으로 참조)
* Deep binding: 실제 실행한 함수가 존재하는 위치에서 static하게 스코프를 결정한다 (코드 상에서 실행된 함수가 정의된 위치 상으로 상위 블록으로 참조)
* Ad hoc binding: 위 두 방식과 달리 코드 상으로 스코프를 결정하지 않는다. 함수가 실행된 call stack을 기준으로 상위 블록으로 간주해서 참조한다.

## Overloaded Subprograms

같은 동일한 스코프 내에서 동일한 이름을 가진 subprogram을 여러 개 정의하는 것을 말한다. 하지만 protocol이 중복되면 안 된다.

함수를 호출할 때, actual parameter의 타입을 보고 호출할 함수를 결정한다.

이때 이슈가 두 가지 있다.

1. coercion을 허용할 것인가? (자동 형변환)
    * 정확히 매칭되는 함수가 없을 경우, 자동 형 변환을 사용할 것인가, 그렇다면 어떻게 매칭시켜 줄 것인가
    * -> 보통 기본적으로 데이터 변환이 더 큰 범위의 데이터로 변환이 가능한 경우 허용한다. 다만, 그때 중복 해석이 되는 경우 에러를 발생시킨다.
2. 파라미터 포맷이 같지만, return type만 다른 경우는 어떻게 처리 할 것인가?
    * -> 보통 어떤 함수를 실행시킬지 알 수 없으므로 에러를 반환한다

## Generic Subprograms

재사용성 (Reusability)는 생산성 (Productivity)에 중요하다.

따라서, 여러 다형성 (Polymorphism)을 지원하는 방법이 필요하다.

1. Ad hoc polymorphism: overloaded subprogram을 말한다.
2. Subtype polymorphism: OOP에서 상위(부모) 객체에서 하위(상속받은 자식)을 접근할 수 있다.
3. Parametric polymorphism: generic subprogram을 말한다.

C++의 template 같은 문법을 Generic subprogram이라고 한다.

```c++
template < calss T >
T max(T x, T y) {
    return x > y ? x : y;
}
max(1, 2);
max(2.0, 1.0);
```

Generic function과 동일한 이름을 가졌지만, 타입이 존재하는 function이 있다면, 해당 함수를 먼저 매칭시킨다. 모두 없다면, 이후 generic function을 매칭시킨다.

C++의 Generic은 Coercion을 허용하지 않는다.

#define같은 매크로로 구현할 수도 있지만, 다음처럼 사용할 경우, 의도치 않은 side effect를 발생시킬 수 있다.

```c++
#define square(x) x * x
int a = 5;
int b = square(a++); // int b = a++ * a++;
```

## User Defined Overloaded Operators

사용자 정의 연산자를 정의할 수 있다.

```c++
class Complex {
    public:
        Complex(int real, int imag) {
            this->real = real;
            this->imag = imag;
        }
        Complex operator+(const Complex& c) {
            Complex temp;
            temp.real = real + c.real;
            temp.imag = imag + c.imag;
            return temp;
        }
    private:
        int real;
        int imag;
};
Complex x1 = Complex(1, 1);
Complex x2 = Complex(2, 2);
Complex x3 = x1 + x2;
```

## Closures

함수가 일급 객체일 경우, 함수를 반환하는 함수를 만들 수 있다.

이때, 내부 함수에서 외부 함수의 변수를 참조하는 것 뿐만 아니라, 외부 함수의 실행이 종료되어도, 외부 함수의 변수를 참조할 수 있다.

```python
def addNumber(fixedNum):
    def add(num):
        return fixedNum + num
    return add
func = addNumber(10)
func(20) # 30
func(30) # 40
```

* 전역 변수 사용을 줄일 수 있다.
* 비슷한 코드의 재사용성을 높일 수 있다.

## Coroutines

코루틴은 특별한 subprogram이다.

* 코루틴은 caller와 callee가 동등한 관계이다. 일반적인 subprogram은 caller와 callee가 상하 관계이다.
* 코루틴은 여러 시작점을 가지고 있을 수 있다.

```python
def coroutine():
    print('callee 1')
    x = yield 1
    print('callee 2: %d' % x)
    x = yield 2
    print('callee 3: %d' % x)

task = coroutine()
i = next(task) # print callee 1, i = 1
i = task.send(10) # print callee 2: 10, i = 2
i = task.send(20) # print callee 3: 20 then stop iteration exception

===
callee 1
callee 2: 10
callee 3: 20
StopIteration
```

---

# \[9주\] Implementing Subprogram

## General Semantics of Calls and Returns

Subprogram은 call과 return의 조합으로 이루어져있다.

### Subprogram call

* Parameter passing 방법이 결정돼야 한다.
* stack-dynamic 지역 변수를 할당하고 대입 (Binding) 해야 한다.
* Execution Status (return address, caller saved register 등)를 저장해야 한다.
* subprogram을 실행할 수 있도록 제어할 수 있어야 한다.
* nested subprogram의 경우 비지역 변수를 접근하는 방법론이 필요하다.

### Subprogram return

* out모드와 in-out모드의 경우 formal parameter를 actual parameter에 대입해야 한다.
* stack-dynamic 지역 변수를 할당 해제 해야한다.
* Execution Status를 복구해야 한다.
* caller로 돌아갈 수 있도록 제어해야 한다.

## Simple subprogram

Simple subprogram이란, nested subprogram을 지원하지 않고, 지역 변수를 사용하기 위해서 stack-dynamic 방식이 아닌 static 방식을 사용하는 subprogram을 말한다.

call과 return은 다음 정보를 저장해야 한다.

* Status information about the caller
* Parameters
* Return address
* Return value for functions
* Temporaries used by the code of the subprograms

Callee의 Linkage action은 다음 두 시간에 발생할 수 있다.

1. Prologue: subprogram이 실행되기 전에 발생한다.
2. Epilogue: subprogram이 종료되기 전에 발생한다.

### Semantic of call

1. Execution status를 저장한다 (caller or callee에 의해)
2. Parameter를 넘겨준다 (caller에 의해)
3. return address를 넘겨준다 (caller에 의해)
4. subprogram을 실행한다 (callee에 의해)

### Semantic of return

1. out모드의 경우 formal parameter를 actual parameter에 대입한다. (callee에 의해)
2. subprogram이 function일 경우 (return value 존재) caller가 return value를 접근할 수 있도록 전달한다. (callee에 의해)
3. Execution status를 복구한다. (callee에 의해)
4. caller로 돌아간다. (callee에 의해)

### Consists of two separate parts (Why two?? it looks like three)

* Actual Code (constant)
* Non-Code: 지역 변수와 데이터 / Mutable하다.
* Activation Record (Non-Code): Non-Code 파트의 포맷과 레이아웃
    * ARI(Activation Record Instance): 포맷을 지키면서 만들어진 인스턴스

|                 |
|-----------------|
| Local Variables |
| Parameters      |
| Return Address  |

> An activation record for simple subprograms

* Simple subprogram의 ARI는 고정 사이즈이다. 그래서 Statically하게 할당할 수 있다.
* Recursion을 지원하지 않는다. Only one ARI is active
* Single Activation Record per subprogram (subprogram이 실행될 때마다 하나의 ARI만 생성된다.)

## Subprograms with Stack-Dynamic Local Variables

Recursion을 제공한다. 하지만, 더 복잡한 Activation Record를 필요로 한다.

* 보통 Activation Record의 포맷은 컴파일 타임에 알 수 있다.
* ARI (Activation Record Instance)는 동적으로 생성되어야 한다.
* Return address, Dynamic link, Parameters는 caller에 의해 ARI에 저장되어야 한다.
    * Return address: caller로 돌아갈 주소
    * Dynamic link: caller의 ARI를 가리키는 포인터
        * Statically-scoped: 디버깅을 위해 사용
        * Dynamically-scoped: 동적인 scope 내에 변수를 찾기 위해 사용
    * Parameters: actual parameter를 저장한다.
    * Local variables: 지역 변수를 저장한다. (단, Scalar type만 저장한다. Structure 타입은 다른 곳에 저장되고, 그를 가리키는 포인터를 저장한다.)

## Subprograms with Stack-Dynamic Local Variables

* Environment Pointer (EP)가 필요하다.
    * EP는 현재 실행 중인 subprogram의 ARI를 가리킨다.
* Subprogram이 호출되면, 현재 EP는 새로운 ARI에 Dynamic Link로 저장된다. 이후 EP는 새로운 ARI를 가리킨다.
* Subprogram이 종료되면, EP는 이전 ARI를 가리킨다.
    * stack top -> EP - 1
    * EP = ARI.dynamic_link

### New Actions in linkage process

새로운 함수가 호출되면,

Caller는 다음과 같은 작업을 수행한다.

1. ARI를 생성한다.
2. Execution Status를 저장한다.
3. Parameter를 넘겨준다.
4. Return address를 넘겨준다.
5. Transfer control to the called. (함수를 실행한다.)

Callee는 다음과 같은 작업을 수행한다.

in the prologue

1. 이전 EP를 스택의 dynamic link로 저장하고, 새로운 값을 만든다.
2. 지역 변수를 할당한다.

in the epilogue

1. out모드의 경우 formal parameter를 actual parameter에 대입한다.
2. 현재 subprogram이 funtcion (return value가 존재)라면, return value를 caller에게 전달한다.
3. stack top = EP - 1로 설정하고, EP를 old dynamic link로 설정한다.
4. Execution status를 복구한다.
5. caller로 돌아간다.

## Nested Subprograms

nested subprogram에서 access를 위해 다음 두 가지 단계가 필요하다.

1. 스택에 어떤 변수가 할당됐는지 ARI에서 찾기 (find ARI in stack in which the variable is allocated)
2. 변수를 ARI 포인터로부터 얼마만큼 이동하면 찾을 수 있는지 찾기 (offset)

????

Finding correct ARI is more interesting

* Only static ancestor scopes are visible (accessible)
* A subprogram is callable only when all of its static ancestor subprograms are active
* Need to find all ARI from the closely nested one

아마 이런 뜻일 거라고 추측함

inner subprogram은 outer subprogram의 변수를 참조할 수 있기 때문에, ARI도 중복해서 사용할 수 있다.  
그렇기 때문에 nested된 모든 ARI를 찾아야 한다.

* 모든 정적인 조상 스코프 (코드 상으로 nested된 부모 스코프)가 visible해야 한다.
* 모든 부모가 실행 중일때만 실행된다. (즉, nested된 부모가 실행되지 않으면 밖에서는 실행할 수 없다.)
* 조상의 지역 변수를 참조해야 하기 때문에 모든 ARI를 찾아야 한다.

### Static chain

Static chain은 static-scoped language에서 사용되는 기법으로, 접근 가능한 nonlocal variable을 정적 분석을 통해 찾을 수 있게 만들어주는 방식이다.

* Static Scope Pointer라고도 불린다.
* Static link를 ARI에 추가해서 Chaining해서 조상의 ARI를 찾을 수 있다.
* static parent의 ARI의 bottom point를 가리킨다.

static chain을 사용할 경우 다음 내용을 고려해야 합니다.

* nonlocal variable을 찾기 위해 코스트가 발생한다.
* 시간이 중요한 프로그램의 경우 코스트를 예측하기 어렵다.

## Blocks

유저가 정의한 로컬 스코프이다.

* 같은 이름을 가진 다른 변수를 가질 수 있다.
* 파라미터가 없는 subprogram으로 처리된다.
* 모든 블록은 ARI를 갖는다.
* Blocks는 더 간단하고 효율적인 방법으로 구현 가능하다.
* ARI에서 local variable 다음에 할당한다.
* Block 내 변수는 지역변수처럼 관리할 수 있다.

## Implementing Dynamic Scoping

Deep Access와 Shallow Access가 존재하지만, Binding과 같은 개념은 아니다.

### Deep Access

* 부모 ARI를 찾을 때 가장 최근에 사용된 ARI를 찾는다.
* 따라서 Dynamic Chain을 사용한다.
* Access를 하기 위해서 모든 stack을 깊게 찾아야 한다.
* 컴파일 타임에 Chain의 Length를 결정할 수 없다. (재귀함수 등이 있어서)
* 재귀함수 같은걸 사용하면 Static Scoped Language보다 검색이 느릴 수 있다.
* ARI는 검색을 위해 변수 이름을 저장해야 한다.

### Shallow Access

Deep Access와 Shallow Accessdml Semantics(의미론)은 같다.

* subprogram 내에 선언된 변수는 ARI에 저장되지 않는다.
* 변수 이름별로 분리된 스택을 갖는다.

---

* Deep Access: subprogram linkage가 빠르지만, 비지역 변수 참조가 느리다.
* Shallow Access: 비지역 참조가 빠르지만, subprogram linkage가 느리다.

# \[9주\] Implementing Subprogram (2) - Abstract Data Types and Encapsulation Constructs

## Abstraction

Entity의 가장 중요한 속성 (Attributes)만 포함하는 방식

여러 새가 있을 때 Common Features는 다음과 같다.

1. two wings
2. two legs
3. a tail
4. feathers
5. ...

서로 다른 새를 포현할 때 위 내용은 스킵할 수 있다. (중복 사용 가능)

Specific Feature는 다음과 같이 분리할 수 있다.

1. Black for crow
2. Striped types of sparrows
3. ...

이렇게 공통된 부분을 추상화하면, 비슷한 타입에 대해서 공통된 부분을 공유해서 사용할 수 있다.

현재는 프로그래밍에서 추상화라는 개념을 사용한다.

### Process Abstraction

* Subprogram
* Sort 등

### Data Abstraction

C의 struct, java의 Object 등으로 데이터를 추상화한다.

## Abstract Data Type (ADT)

### Language Defined Types as ADT

* Floating point type
    * 수학적인 유리수 타입