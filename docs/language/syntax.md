# Lala Syntax

Lala's syntax is designed to be as minimal and readable as possible. It completely removes the visual noise of traditional C-family languages.

## 1. No Semicolons
Statements are terminated by a newline. Do not use semicolons `;`.

```lala
// Correct
number age = 20
print(age)

// Incorrect
number age = 20;
```

## 2. Indentation-Based Blocks
Scope is defined by colons `:` and indentation, exactly like Python. There are no curly braces `{}`.

```lala
// Correct
agar age > 18:
    print("Adult")
warna:
    print("Minor")
```

## 3. No Parentheses for Control Flow
Control statements do not require surrounding parentheses.

```lala
// Correct
agar age > 18:
    print("Adult")

// Incorrect
agar (age > 18):
    print("Adult")
```

## 4. Full UTF-8 Support
Lala source files are strictly UTF-8. Identifiers, strings, and comments can contain any valid Unicode characters, which is essential for native Hindi developers.

```lala
string नाम = "राम"
print(नाम)
```

## 5. Comments
Single-line comments start with `#`. Multi-line block comments are enclosed in `###`.

```lala
# This is a single-line comment
number x = 5

###
This is a 
multi-line block comment
###
```
