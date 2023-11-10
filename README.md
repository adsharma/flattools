# Flattools - collection of tools to deal with Flatbuffers

[Flatbuffers](https://github.com/google/flatbuffers) is a cross platform serialization library
with a focus on zero copy deserialization. They're similar in functionality to protocol buffers and
thrift, but with a focus on gaming related use cases where the CPU cost of decoding large buffers
can be significant.

Flattools implements an alternative flatbuffers compiler implemented in python, referred to as
`flatc.py`. The idea is that we could use flatbuffers as a
[serialization agnostic](https://adsharma.github.io/flattools/) IDL.

Why is this important? Building software around a well defined type system that expresses
various concepts in a given domain such as banking or gaming (also knows as domain driven design)
is a useful technique, but [somewhat controversial](https://adsharma.github.io/flattools-programs/).


## Usage

Installing

``` {.sourceCode .bash}
pip3 install flattools
```

Running

``` {.sourceCode .bash}
$ ~/.local/bin/flatc tests/parser-cases/color.fbs --kotlin=1
```

Generates something like

``` {.sourceCode .kotlin}
    // automatically generated by the FlatBuffers compiler, do not modify
    enum class Color(val x: Byte) {
        Red(1),
        Green(2),
        Blue(3),
    }

    data class Person(
        val name: String,
        val address: String,
        val age: Short,
        val length: ULong,
        val favorite_color: Color,
    )

    data class Product(
        val label: String,
        val price: Int,
    )

    sealed class Item {
        class Product : Item()
        class Person : Item()
    }
```

This uses templated code generation using jinja2.

Supported languages: python, rust, kotlin, swift

## Supporting new languages

Pull requests are welcome for other languages. The idea is to start
from one of the existing languages [here](https://github.com/adsharma/flattools/tree/master/lang)
and creating a [new template](https://github.com/adsharma/flattools/tree/master/templates) for
your language of choice.

There are existing tests, so all you need to do is generate [golden/expected](https://github.com/adsharma/flattools/tree/master/tests/expected)
data for your language of choice