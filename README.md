# BhauLang

BhauLang is a toy programming language inspired by BhaiLang. It includes basic constructs for variable declaration, printing, conditionals, and loops.

## Features

- Variable declaration
- Printing to the console
- Conditional statements (`if`, `else if`, `else`)
- While loops

## Installation

You can install BhauLang directly from PyPI:

```sh
pip install BhauLang
```

## Usage
After installing the package, you can run .bhau files using the bhau command. For example:

```sh
bhau example.bhau
```

## Syntax

### Variable Declaration
Declare a variable using he bagh followed by the variable name and value:

```sh
he bagh a = 10
he bagh name = "hello"
```

he bagh: This keyword is used to declare a new variable.

### Printing
Print to the console using bol:

```sh
bol (a)
bol ("Hello, world!")
```

bol: This keyword is used to print the value of an expression or variable to the console.

### Conditionals
Use jar, nasel tar, and nahi tar for conditional statements:

```sh
jar (a < 10) {
    bol ("yes less than 10")
}
nasel tar (a < 20) {
    bol ("yes less than 20")
}
nahi tar {
    bol ("not less than 10 or 20")
}
```

- jar: This keyword is used for the if condition. If the condition is true, the block of code within the braces {} is executed.
- nasel tar: This keyword is used for the else if condition. If the previous if or else if condition was false, and this condition is true, the block of code within the braces {} is executed.
- nahi tar: This keyword is used for the else condition. If none of the previous if or else if conditions were true, the block of code within the braces {} is executed.

### While Loops
Use joparyanta for while loops:

```sh
joparyanta (a < 5) {
    bol (a)
    a = a + 1
}
```

joparyanta: This keyword is used for a while loop. The loop continues to execute the block of code within the braces {} as long as the condition is true.


## Examples
- Example 1 : 
```
he bagh a = 10
bol (a)
jar (a<10){
    bol ("yes less than 10")
}
nasel tar (a<20){
    bol ("yes less than 20")
}
nahi tar{
    bol ("not less than 10 or 20")
}

```

Expected Output:

```sh
10
yes less than 20
```
- Example 2
```sh
he bagh name = "hello" 
bol (name)
he bagh number = 56
bol (number)
```

Expected Output:
```sh
hello
56
```

- Example 3
```sh
he bagh a = 0
joparyanta ( a<5 ){
    bol (a)
    a = a + 1
}
```

Expected Output:

```
0
1
2
3
4
```


- Example 4
```sh
he bagh countdown = 4
joparyanta (countdown > 0){
    bol (countdown)
    countdown = countdown - 1
}
```

Expected Output:

```
4
3
2
1
```
`BhauLang does not handle errors gracefully. It may crash or produce unexpected behavior if incorrect syntax or unsupported features are encountered.`