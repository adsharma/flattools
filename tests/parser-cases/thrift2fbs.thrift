struct Person {
    1: string name,
    2: string address,
    3: i16 age
}

struct Email {
    1: string subject = 'Subject',
    2: string content,
    3: Person sender,
    4: required Person recver,
}
