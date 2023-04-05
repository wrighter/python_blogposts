<div class="cell markdown" markdown="1">

# A Gentle Introduction to Structural Pattern Matching in Python

When new features are added to Python, sometimes it can take a while to learn about and start using the feature. For me, structural pattern matching is a good example. Some features are very easy to grasp and start using (for example, f-strings), but structural pattern matching can be confusing for developers who have not been exposed to it before. Some try to relate it to the wrong language feature in their past experience. In this article, I'll introduce a few foundational concepts about the feature, then describe it in more detail, and provide some practical examples of how to use it.

Structural pattern matching was first made available in Python 3.10. Functional programming languages such as scala make heavy use of structural pattern matching, and Python's implementation is influenced by ideas from other languages. If you haven't used this feature in another language before, hopefully this article will introduce it to you and show you how it can be useful in your own work.

In order to run the code in this article, you have to be running Python 3.10 or above or you will get the following error on the `match` statement: `SyntaxError: invalid syntax`.

To install Python 3.10, I recommend using [pyenv](https://www.wrighters.io/you-can-easily-and-sensibly-run-multiple-versions-of-python-with-pyenv/). Pyenv allows you to have multiple versions of Python on your workstation. Here's what I did to install 3.10.4 on my laptop after installing Pyenv. (3.10.4 was the latest version of 3.10 when I wrote this, you might choose to install any version above 3.10.0).

``` shell
pyenv install 3.10.4
```

Then, I used [pyenv-virtualenv](https://www.wrighters.io/use-pyenv-and-virtual-environments-to-manage-python-complexity/) to make a virtual environment to work with the new 3.10 install.

``` shell
pyenv virtualenv 3.10.4 python-matching
pyenv activate python-matching
```

If you installed Python another way, you can use that version to follow along, as long as it's 3.10 or above.

## The basics

What is Structural Pattern Matching? Before we get to that, let's back up and start with a few Python basics first. As I was reading about this feature, I found a review of these topics helpful.

You've probably seen this done in Python before:

</div>

<div class="cell code" markdown="1" execution_count="1">

``` python
values = [1, 2, 3]

a, b, c = values
print(a, b, c, values)
```

<div class="output stream stdout" markdown="1">

    1 2 3 [1, 2, 3]

</div>

</div>

<div class="cell markdown" markdown="1">

What we've done here is created three new variables called `a`, `b`, and `c` that point to elements in the list `values`.

What happens if we try to assign more variables than exist?

</div>

<div class="cell code" markdown="1" execution_count="2">

``` python
a, b, c, d = values
```

<div class="output error" markdown="1" ename="ValueError" evalue="not enough values to unpack (expected 4, got 3)">

    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
    Cell In[2], line 1
    ----> 1 a, b, c, d = values

    ValueError: not enough values to unpack (expected 4, got 3)

</div>

</div>

<div class="cell markdown" markdown="1">

And what about fewer than exist?

</div>

<div class="cell code" markdown="1" execution_count="3">

``` python
a, b = values
```

<div class="output error" markdown="1" ename="ValueError" evalue="too many values to unpack (expected 2)">

    ---------------------------------------------------------------------------
    ValueError                                Traceback (most recent call last)
    Cell In[3], line 1
    ----> 1 a, b = values

    ValueError: too many values to unpack (expected 2)

</div>

</div>

<div class="cell markdown" markdown="1">

However, you can match multiple elements in a single variable using a `*`. The variable `rest` will be a list with the rest of the values.

</div>

<div class="cell code" markdown="1" execution_count="4">

``` python
a, *rest = values
print(a, rest)
```

<div class="output stream stdout" markdown="1">

    1 [2, 3]

</div>

</div>

<div class="cell markdown" markdown="1">

OK, so let's say that we have a list and we want to take different actions when we have 1, 2, 3, or more values in the list. How would you write this?

Based on what we've already seen and a few else/if/elif statements, we could do something like this:

</div>

<div class="cell code" markdown="1" execution_count="5">

``` python
a = None
b = None
c = None
d = None
if len(values) == 1:
    a = values[0]
    print("One behavior")
elif len(values) == 2:
    a, b = values
    print("Two behavior")
elif len(values) == 3:
    a, b, c = values
    print("Three behavior")
elif len(values) >= 4:
    a, b, c, *d = values
    print("More behavior")
```

<div class="output stream stdout" markdown="1">

    Three behavior

</div>

</div>

<div class="cell markdown" markdown="1">

## Enter the structural matching statement

Now this might look sort of terrible, and you might have a few thoughts on how to make this code better, but really, there's not much else you can do in Python to handle all these situations. Most of us have just rolled up our sleeves and written this sort of code.

Now if you come from a C/C++/Java background, you might think this is where a `switch` statement would be handy. If you recall, a `switch` statement allows you to essentially write a series of `if/else` statements in more concise syntax. You could switch on the length of the values list, for example, and avoid the multiple `len` checks.

When Python introduced the `match` statement, many people were confused and thought of it strictly as a `switch` statement. Instead of just showing you lots of working correct examples, I'm going to show you a few mistakes first so you can be familiar with errors you could see.

In terms of syntax, the `match` statement requires a subject expression to match on, followed by one or more `case` blocks. So you could try something like this:

</div>

<div class="cell code" markdown="1" execution_count="6">

``` python
match len(values):
    case 1: print("One behavior")
    case 2: print("Two behavior")
    case 3: print("Three behavior")
```

<div class="output stream stdout" markdown="1">

    Three behavior

</div>

</div>

<div class="cell markdown" markdown="1">

While using the match statement with literal values (we used `1`, `2`, and `3` above) in the case blocks technically works, that's really a basic case. This is not really much better than just using `if/else/elif` blocks. If you try to make use of `match` in this way, you might get really confused at some errors you find. For example, let's say you try to do this:

</div>

<div class="cell code" markdown="1" execution_count="7">

``` python
ONE = 1
TWO = 2
THREE = 3

match len(values):
    case ONE: print("One behavior")
    case TWO: print("Two behavior")
    case THREE: print("Three behavior")
```

<div class="output error" markdown="1" ename="SyntaxError" evalue="name capture 'ONE' makes remaining patterns unreachable (321946147.py, line 6)">

      Cell In[7], line 6
        case ONE: print("One behavior")
             ^
    SyntaxError: name capture 'ONE' makes remaining patterns unreachable

</div>

</div>

<div class="cell markdown" markdown="1">

What is happening here? Why is this any different from the code above it? Well, this is a case of not understanding what structural pattern matching is intended to do. It's not intended to be used strictly as a `switch`. This error message might be a bit confusing. What it is saying is that you have three branches of your match that are all trying to match the same thing: a case where the length of the `values` list can be *assigned to* a single variable. This is not checking the *value* of the length of `values`. There is a way to do that, however, if you needed to. You have to use dotted notation so that Python knows you are trying to use a constant value.

</div>

<div class="cell code" markdown="1" execution_count="8">

``` python
class Constants:
    ONE = 1
    TWO = 2
    THREE = 3

match len(values):
    case Constants.ONE: print("One behavior")
    case Constants.TWO: print("Two behavior")
    case Constants.THREE: print("Three behavior")
```

<div class="output stream stdout" markdown="1">

    Three behavior

</div>

</div>

<div class="cell markdown" markdown="1">

So you *can* use `match` as a switch if you really want to. But it's much more powerful than that.

### Matching on patterns

Now that we've fumbled around a bit, instead of using `match` like a simple `switch` statement, we will match on patterns. Thinking back to our earlier examples of unpacking a list, let's use `match` to do this.

</div>

<div class="cell code" markdown="1" execution_count="9">

``` python
# change up the list so you can see we really assigning and retaining the values
values = [19, 30, 1] 
match values:
    case a, b, c:
        print("Found 3: ", a, b, c)
```

<div class="output stream stdout" markdown="1">

    Found 3:  19 30 1

</div>

</div>

<div class="cell markdown" markdown="1">

Note that the variables `a`, `b`, and `c` survive outside the scope of the `match` statement.

</div>

<div class="cell code" markdown="1" execution_count="10">

``` python
print(a, b, c)
```

<div class="output stream stdout" markdown="1">

    19 30 1

</div>

</div>

<div class="cell markdown" markdown="1">

Great, let's make it match on lists of up to four elements

</div>

<div class="cell code" markdown="1" execution_count="11">

``` python
match values:
    case a:
        print("1 - ", a)
    case a, b:
        print("2 - ", a, b)
    case a, b, c:
        print("3 - ", a, b, c)
    case a, b, *c:
        print("4 - ", a, b, c)
```

<div class="output error" markdown="1" ename="SyntaxError" evalue="name capture 'a' makes remaining patterns unreachable (1371129738.py, line 2)">

      Cell In[11], line 2
        case a:
             ^
    SyntaxError: name capture 'a' makes remaining patterns unreachable

</div>

</div>

<div class="cell markdown" markdown="1">

Wait, why wouldn't that work? What does that error mean? Shouldn't we be able to match on any of the four?

What's happening here is that the first match will make all other patterns unreachable - because it will *always* match. We are matching the variable `values` on a new variable name `a`, so this is basically the same as saying `a = values`, which will always work. If you want to match a on a ist with one element, just say so.

</div>

<div class="cell code" markdown="1" execution_count="12">

``` python
match values:
    case [a]:
        print("1 - ", a)
    case a, b:
        print("2 - ", a, b)
    case a, b, c:
        print("3 - ", a, b, c)
    case a, b, *c:
        print("4 or more - ", a, b, c)
```

<div class="output stream stdout" markdown="1">

    3 -  19 30 1

</div>

</div>

<div class="cell markdown" markdown="1">

You can also do it in varying combinations of `[]` or `()` like this:

</div>

<div class="cell code" markdown="1" execution_count="13">

``` python
match [1,2,3,4,5]:
    case [a]:
        print("1 - ", a)
    case [a, b]:
        print("2 - ", a, b)
    case (a, b, c):
        print("3 - ", a, b, c)
    case a, b, *c:
        print("4 or more - ", a, b, c)
```

<div class="output stream stdout" markdown="1">

    4 or more -  1 2 [3, 4, 5]

</div>

</div>

<div class="cell markdown" markdown="1">

Also, note that there are no errors or warnings if you don't match anything. Scala developers will cringe a bit at this. Since Scala has strong typing, it can enforce that every possible match type is covered.

</div>

<div class="cell code" markdown="1" execution_count="14">

``` python
match values:
    case [a, b]:
        print("2 - ", a, b)
```

</div>

<div class="cell markdown" markdown="1">

But you can include a case using `_` that will capture anything not captured above it. It's required to be the last `case` statement in the `match`.

</div>

<div class="cell code" markdown="1" execution_count="15">

``` python
match values:
    case [a, b]:
        print("2 - ", a, b)
    case _:
        print(values, "not matched")
```

<div class="output stream stdout" markdown="1">

    [19, 30, 1] not matched

</div>

</div>

<div class="cell markdown" markdown="1">

Let's make a full example of what we were trying to do earlier, but with the `match` statement.

</div>

<div class="cell code" markdown="1" execution_count="16">

``` python
match values:
    case [a]:
        print("One behavior", a)
    case [a, b]:
        print("Two behavior", a, b)
    case [a, b, c]:
        print("Three behavior", a, b, c)
    case [a, b, c, *d]:
        print("More behavior", a, b, c, d)
    case _:
        print(values, "not matched")
```

<div class="output stream stdout" markdown="1">

    Three behavior 19 30 1

</div>

</div>

<div class="cell markdown" markdown="1">

## A concrete example

Now that we have the basics mastered, let's dive in and see the true power of structural pattern matching. What we've covered so far is just the basics. We can do much more with structural pattern matching.

You have already seen how we can match on a sequence of various sizes. Let's layer on more complex functionality. Let's say that you have a configuration for an application, perhaps something that is stored in a configuration file or a database. You need to use this configuration to properly configure and run your application. Over the course of several steps, we will build up a more complicated configuration and show how structural pattern matching will make our code more readable and maintainable. For each step, I'll create two ways of processing the configuration and you can decide which works better.

Fist, let's create a very basic configuration, where we have the user and role in two variables. For this first step, we want to validate the `role` of the user, ensuring it is one of the valid roles of `admin`, `user`, and `power_user`.

</div>

<div class="cell code" markdown="1" execution_count="17">

``` python
role = 'admin'
user = 'John'


def set_admin_status(user) -> None:
    # pretend this does something useful
    print(f"{user} is now able to do admin stuff")

def set_power_user_status(user) -> None:
    # pretend this does something useful
    print(f"{user} is now able to do power user stuff")


# this is the old way
def process_role(role, user) -> None:
    if role == 'admin':
        set_admin_status(user)
    elif role == 'user':
        # default behavior
        pass
    elif role == 'power_user':
        set_power_user_status(user)
    else:
        # could raise an exception here
        print("Unknown role", role)

# this is with structural pattern matching
def process_role_match(role, user) -> None:
    match role:
        case 'admin':
            set_admin_status(user)
        case 'user':
            # default behavior
            pass
        case 'power_user':
            set_power_user_status(user)
        case _:
            # could raise an exception here
            print("Unknown role", role)


process_role(role, user)
process_role(role, user)
```

<div class="output stream stdout" markdown="1">

    John is now able to do admin stuff
    John is now able to do admin stuff

</div>

</div>

<div class="cell markdown" markdown="1">

OK, I prefer the second option here, but mostly because I'm familiar with `match` already. There's very little difference in the amount of code needed to process the configuration.

## Matching on values in lists

Now let's look at an example of a list of values. Let's say that there's a font setting, with an optional font weight. Let's also say that we need to check for an unlicensed font setting and update it if we see it before calling `set_font`.

</div>

<div class="cell code" markdown="1" execution_count="18">

``` python
font_settings = ['SuperFont', 14]

def set_font(font, weight=12) -> None:
    # pretend this does something useful
    print(f"Font set to {font} {weight}")

# this is the old way
def process_font(font_settings) -> None:
    if len(font_settings) >= 1:
        font = font_settings[0]
        if font == "SuperFont":
            font = "Arial"
    if len(font_settings) == 1:
        set_font(font)
    elif len(font_settings) == 2:
        _, weight = font_settings
        set_font(font, weight)
    else:
        # could raise an exception here
        print("Unknown font settings", font_settings)


# this is with structural pattern matching
def process_font_match(font_settings) -> None:
    match font_settings:
        case ["SuperFont", *rest]:
            font = "Arial"
            weight = 12 if len(rest) == 0 else rest[0]
            set_font(font, weight)
        case [font]:
            set_font(font)
        case [font, weight]:
            set_font(font, weight)
        case _:
            # could raise an exception here
            print("Unknown font settings", font_settings)

process_font(font_settings)
process_font_match(font_settings)
process_font(["Times New Roman"])
process_font_match(["Times New Roman"])
process_font(["Times New Roman", 16])
process_font_match(["Times New Roman", 16])
```

<div class="output stream stdout" markdown="1">

    Font set to Arial 14
    Font set to Arial 14
    Font set to Times New Roman 12
    Font set to Times New Roman 12
    Font set to Times New Roman 16
    Font set to Times New Roman 16

</div>

</div>

<div class="cell markdown" markdown="1">

Note how I made use the of a match on literal values to check for the exceptional case first. Both sets of code are a bit messy, but I'd say the intention of the matching code is clearer. Imagine how this could get more complicated with more unique sets of circumstances for different font choices.

## Matching on `dict`s

We'll now look at how to match on mappings, such as a Python `dict`. This is a very typical use case in Python. We often have to inpect the contents of a `dict` and act accordingly.

Let's imagine we store some configuration in a `dict` that can be sparsely populated but has multiple levels. It also needs to be validated and used for configuration.

Since it can be sparse, we need to properly check for the values in the `dict`, we can't just assume they are present. Since it is not strongly typed, we need to do our own checking that `int` values are valid, or enumerated values match something in the possible values, etc. This can be a bit cumbersome.

But with pattern matching, we have the ability to match on the contents of the `dict`, including the types of the values. We'll leverage this even more in a bit, but for now, let's just use the builtin type of `int` and `str` to check the types of the values. For example, you can match on an `int` value like this, and be assured that `volume` will be a valid int:

``` python
case {"volume": int(volume)}:
    print(volume)
```

We can also verify that values are valid within the `case` statement itself, and be assured that the value will be what is expected.

``` python
case {"orientation": ("landscape" | "portrait") as orientation}:
    print(orientation)
```

This could also be done like this:

``` python
case {"orientation": orientation} if orientation in ["landscape", "portrait"]:
    print(orientation)
```

Let's build two versions to process a multi-level configuration `dict`.

</div>

<div class="cell code" markdown="1" execution_count="19">

``` python
options = {
    'sound': {
        'volume': 50,
        'equalizer': {
            'bass': 50,
            'treble': 50
        }
    },
    'display': {
        'brightness': 50,
        'orientation': 'landscape'
    }
}

# common functions for setting values
#
def set_sound_volume(volume: int) -> None:
    # pretend this does something useful
    print(f"Sound volume set to {volume}")

def set_sound_equalizer(bass: int, treble: int) -> None:
    # pretend this does something useful
    print(f"Sound equalizer set to bass: {bass}, treble: {treble}")

def set_display_brightness(brightness: int) -> None:
    # pretend this does something useful
    print(f"Display brightness set to {brightness}")

def set_display_orientation(orientation: str) -> None:
    # pretend this does something useful
    print(f"Display orientation set to {orientation}")

# this is the old way
def process_options(options: dict) -> None:
    # we can do it with a lot of checks!
    sound = options.get('sound', {})
    if 'volume' in sound:
        try:
            volume = int(sound['volume'])
            set_sound_volume(volume)
        except ValueError:
            pass
    if 'equalizer' in sound:
        equalizer = sound['equalizer']
        if 'bass' in equalizer:
            try:
                bass = int(equalizer['bass'])
                if 'treble' in equalizer:
                    treble = int(equalizer['treble'])
                    set_sound_equalizer(bass, treble)
            except ValueError:
                pass
    if 'display' in options:
        display = options['display']
        if 'brightness' in display:
            try:
                brightness = int(display['brightness'])
                set_display_brightness(brightness)
            except ValueError:
                pass
        if 'orientation' in display:
            try:
                orientation = str(display['orientation'])
                if orientation in ['landscape', 'portrait']:
                    set_display_orientation(orientation)
                else:
                    print("Unknown orientation", orientation)
            except ValueError:
                pass

def process_options_match(options: dict) -> None:
    match options.get('sound'):
        case {'volume': int(volume), 'equalizer': {'bass': int(bass), 'treble': int(treble)}}:
            set_sound_equalizer(bass, treble)
            set_sound_volume(volume)
        case {'volume': volume}:
            set_sound_volume(volume)
        case _:
            print("Invalid sound options", options.get('sound'))
    match options.get('display'):
        case {'brightness': int(brightness), 'orientation': ('landscape' | 'portrait') as orientation}:
            set_display_brightness(brightness)
            set_display_orientation(orientation)
        case {'brightness': int(brightness)}:
            set_display_brightness(brightness)
        case {'orientation': orientation} if orientation in ['landscape', 'portrait']:
            set_display_orientation(orientation)
        case _:
            print("Invalid display options", options.get('display'))

print("Old way")
process_options(options)
print("New way")
process_options_match(options)
```

<div class="output stream stdout" markdown="1">

    Old way
    Sound volume set to 50
    Sound equalizer set to bass: 50, treble: 50
    Display brightness set to 50
    Display orientation set to landscape
    New way
    Sound equalizer set to bass: 50, treble: 50
    Sound volume set to 50
    Display brightness set to 50
    Display orientation set to landscape

</div>

</div>

<div class="cell markdown" markdown="1">

The difference between the two values now is much more stark. Being able to match on different combinations of values in the `dict` allows for code to be much more clear and concise. Handling all the possible failures for failed numeric conversions go away. We could also place default values or error handling right where it is needed, instead of mixing it up throughout deeply nested `if/else` statements. The example above is not doing complete error handling, but adding it is much more clear with structural pattern matching.

### Matching on objects

For the last example, we will create our own types and match on them. Let's say that our application has notification options, and they are represented by a class heirarchy that has two levels: a `Notification` base class and subclasses for the different types. They may have some common behavior, but we may also need to handle them differently, including looking at their internal values for proper configuration.

</div>

<div class="cell code" markdown="1" execution_count="20">

``` python
from dataclasses import dataclass

@dataclass
class Notification:
    def notify(self) -> None:
        pass
    pass

@dataclass
class EmailNotification(Notification):
    email: str

@dataclass
class SMSNotification(Notification):
    phone: str
    country_code: int

@dataclass
class SlackNotification(Notification):
    channel: str


config = {
    'notifications': [EmailNotification('joe@example.com'), SMSNotification(123456789, 1), SlackNotification('#general'), SMSNotification(987654321, 44)]
}

def configure_email(email: EmailNotification) -> None:
    # pretend this does something useful
    print(f"Email configured for {email.email}")

def configure_sms(sms: SMSNotification) -> None:
    # pretend this does something useful
    print(f"Domestic SMS configured for [{sms.country_code}]{sms.phone}")

def configure_international_sms(sms: SMSNotification) -> None:
    # pretend this does something useful
    print(f"International SMS configured for [{sms.country_code}]{sms.phone}")

def configure_slack(channel: str) -> None:
    # pretend this does something useful
    print(f"Slack configured for {channel}")

# this is the old way
def process_config(config: dict) -> None:
    notifications = config.get('notifications', [])
    for notification in notifications:
        if isinstance(notification, EmailNotification):
            configure_email(notification)
        elif isinstance(notification, SMSNotification):
            if notification.country_code == 1:
                configure_sms(notification)
            else:
                configure_international_sms(notification)
        elif isinstance(notification, SlackNotification):
            configure_slack(notification.channel)
        else:
            print(f"Unknown notification type {type(notification)}")

# this is with structural pattern matching
def process_config_match(config: dict) -> None:
    for notification in config.get('notifications', []):
        match notification:
            case EmailNotification(_):
                configure_email(notification)
            case SMSNotification(_, 1):
                configure_sms(notification)
            case SMSNotification(_, _):
                configure_sms(notification)
            case SlackNotification(channel):
                configure_slack(channel)
            case _:
                print(f"Unknown notification type {type(notification)}")

print("Old way")
process_config(config)
print("New way")
process_config_match(config)
```

<div class="output stream stdout" markdown="1">

    Old way
    Email configured for joe@example.com
    Domestic SMS configured for [1]123456789
    Slack configured for #general
    International SMS configured for [44]987654321
    New way
    Email configured for joe@example.com
    Domestic SMS configured for [1]123456789
    Slack configured for #general
    Domestic SMS configured for [44]987654321

</div>

</div>

<div class="cell markdown" markdown="1">

Again, the use of `match` here provides much more readable and clean code. There is not one use of `isinstance`, and differentiating between different types of `SMSNotification` values is much more clear.

I'll quickly point out that in order for your own types to match on their values, you either need to use `dataclasses` (as I did above) or create a special `__match__args__` attribute in your own classes if you have multiple arguments you want to match up with using different names. You can read the specs (linked below) for more details.

## Expression vs. Statement [expression-vs-statement]

In other languages, like Scala, a match is an expression instead of a statement so you use it to set values. This can be very handy. You typically do something like this:

``` scala
val label = match token {
    case Name(first, last) => first
    case Title(title)      => title
    case _                 => "[N/A]" 
}
```

In Python, you'd have to rely on something like this (which is not as well contained).

</div>

<div class="cell code" markdown="1" execution_count="21">

``` python
@dataclass
class Name:
    first: str
    last: str

@dataclass
class Title:
    title: str
token = Name('Joe', 'Smith')

label = None

match token:
    case Name(first, last):
        label = first
    case Title(title):
        label = title
    case _:
        label = "[N/A]"

print(label)
```

<div class="output stream stdout" markdown="1">

    Joe

</div>

</div>

<div class="cell markdown" markdown="1">

## Summary

If you are interested in digging into Structural pattern matching more, then there are some good resources available. To prepare this article, I read the following PEPs:

-   syntax proposal [PEP 622](https://peps.python.org/pep-0622)
-   technical spec [PEP 634](https://peps.python.org/pep-0634)
-   motivation and rationale [PEP 635](https://peps.python.org/pep-0635)
-   tutorial [PEP 636](https://peps.python.org/pep-0636/)

By reading this far, you've seen a *lot* of examples. I hope you've learned something about how structural pattern matching works in Python and how it can help you write cleaner, more maintainable, and more understandable code.

</div>
