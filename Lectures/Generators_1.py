def my_three_step_generator():
    print("Just started")
    yield 1
    print("Second step")
    yield 2
    print("The last one")
    yield 3


for i in my_three_step_generator():
    print(i)