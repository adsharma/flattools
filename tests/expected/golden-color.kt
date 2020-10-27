// automatically generated by the FlatBuffers compiler, do not modify
enum class Color(val x: Byte) {
    Red(1),
    Green(2),
    Blue(3),
}

data class Person(
    val name: String,
    val address: String?,
    val age: Short?,
    val length: ULong?,
    val favorite_color: Color,
)

data class Product(
    val label: String?,
    val price: Int?,
)

sealed class Item {
    class Product : Item()
    class Person : Item()
}
