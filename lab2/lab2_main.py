from lab2_phonebook import Phonebook

pb = Phonebook(3)

persons = [
    ["Назар", "+380 00 000 0001"],
    ["Максим", "+380 00 000 0002"],
    ["Агата", "+380 00 000 0003"],
    ["Анастасія", "+380 00 000 0004"],
    ["Євген", "+380 00 000 0005"],
    ["Олег", "+380 00 000 0006"],
    ["Ліза", "+380 00 000 0007"]    
]

for name, phone in persons:
    pb.insert(name, phone)

print(pb.search("Євген"))
print(pb.search_greater_than("Ліза"))
print(pb.search_less_than("Євген"))
