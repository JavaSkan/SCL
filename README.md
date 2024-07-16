# What is SCL ?

SCL (Skanders Command-based Language) is a language that executes command-like
instructions (similarly to a script shell). The idea originated be wanting to
create a language like assembly, but much more efficient, safe and "readable"

# Why ?

This is made for fun, and it's not, by any means, a serious project. I just started it when I began
coding in python, so I can learn through the language and get used to it (mechanics, tips and tricks, the syntax...), 
since I first started with Java, C, C++ etc.

# Does it have a purpose ?

No. I am still thinking of what this language can do and for what. But it will probably remain
without purpose. I don't want it to get more specific in what it can do, because as I said, this is made for fun,
and you can surely guess why by just seeing how messy and unorganized the code is 😅

### Pull requests ?

I am not accepting any pull requests or things like that, even though the code may be better and cleaner. This is a personal project
and I want to progress alone. It is public to see, but it's not subject to any change by any other person than me. (As if I expect people coming
to see my code lol, but if it happens, you know the answer)

# Examples

These are brief examples of the most basic things you can do with SCL

## Variables

---------------------------------------------

### Creating variables
```
new mut int x 0
```
> This creates a variable 'x' of type int that is mutable (can be changed), mut is called a
> variable kind (mut for mutable, const for constant, temp for temporary (not implemented yet))

These are the datatypes for creating a variable:
1. **int** for integer
2. **flt** for float
3. **str** for string
4. **bool** for boolean

* Setting a variable to a value
```
set x 2
```
> This changes the content of the variable (from 0 to 2)

### Variable referencing

Variable referencing is a way to get the value of a variable, by just typing `$<identifer>` where
`<identifier>` is the name of the variable, if it is not existing, the language will throw an error.

Variable referencing is used by many commands at different and specific places, you can know where to use it
if you type `help <command>` in the `NOTE` section

**eg:**
```
dpl $x
```
**Result:**
```
5
```
### Deleting a variable
```
del x
```
> This will delete the variable x from the 'memory', and you can no longer use it, otherwise the language will throw an error

---------------------------------------------

## Display

### Display something in the console:
```
dpl "Hello World!"
```
**Result:**
```
Hello World!
```
> There is two ways you can display things, either be the command 'dpl' or 'dp' which is like
> 'dp' but without a line break

---------------------------------------------

## Loops

### loop command:
```
loop 3 {dpl "Hello World!"}
```
**Result:**
```
Hello World!
Hello World!
Hello World!
```
> As you might've guessed, this executes instructions in the command's body ({...} is called a body)
> for a fixed amount of times (here it's 3). And by the way, we can use boolean values instead of integers
> and the loop command will act like a while loop. Although boolean variables and literals ('true' or 'false')
> exist in the language, there is no implementation of a boolean system yet (apart from using the set command to
> change a variable value).

### foreach command:
```
arr new int myarray [1,2,3]
foreach e in myarray {dpl $e}
```
**Result:**
```
1
2
3
```
> Foreach command iterates over each element of the array, and each value
> is stored in a variable (here it's 'e')

---------------------------------------------

## Exiting

If you want to exit the program, just type `end 0 false`. If you want to know why I typed
`0` and `false`: type `help end`