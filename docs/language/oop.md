# Lala Object Orientation

Lala rejects classical inheritance in favor of composition and interfaces. There is no `extends` or `super` keyword. 

## 1. Classes (`varg`)

A `varg` (class) is a container for data and behavior. 

```lala
varg Player:
    string name
    number health

    kaam jump():
        print(name + " jumped!")
```

### Instantiation
Classes are instantiated by calling them like a function. 
```lala
p = Player()
p.name = "Dheeraj"
p.jump()
```
*Note: Memory is managed automatically. There is no `new` keyword.*

## 2. Interfaces (`swaroop`)

A `swaroop` (interface) defines a contract of behavior. It contains function signatures without implementation.

```lala
swaroop Drawable:
    kaam draw()
```

### Duck Typing
Lala uses structural typing (often called "duck typing"). A `varg` does not need to explicitly declare that it implements a `swaroop`. If the `varg` has the matching functions, it satisfies the interface.

```lala
varg Circle:
    kaam draw():
        print("Drawing a circle")

// Circle implicitly satisfies the Drawable swaroop
```

## 3. Composition

Instead of inheriting from a base class, a `varg` should contain instances of other `varg`s.

**Bad (Inheritance - Not supported in Lala):**
```lala
// This is illegal syntax
varg Dragon extends FlyingMonster:
    ...
```

**Good (Composition):**
```lala
varg FlyingStats:
    number speed
    number altitude

varg Dragon:
    FlyingStats flight
    number fire_damage

    kaam attack():
        print("Dragon attacks from altitude " + flight.altitude)
```
