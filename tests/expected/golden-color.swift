// automatically generated by the FlatBuffers compiler, do not modify
enum Color : Int8 {
    case Red = 1,
    Green = 2,
    Blue = 3
}

protocol NamedAnimal {
    var name: String
    var age: Int16
}

struct Animal {
    var name: String
    var length: UInt64
}

struct Person: Animal {
    var address: String
    var age: Int16
    var favorite_color: Color
}

struct Product {
    var label: String
    var price: Int
}

enum Item {
    case Product(Product)
    case Person(Person)
}