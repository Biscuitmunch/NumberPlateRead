import os
from threading import Thread

def task1():
    os.system("python CS373LicensePlateDetection.py numberplate1.png")

def task2():
    os.system("python CS373LicensePlateDetection.py numberplate2.png")

def task3():
    os.system("python CS373LicensePlateDetection.py numberplate3.png")

def task4():
    os.system("python CS373LicensePlateDetection.py numberplate4.png")

def task5():
    os.system("python CS373LicensePlateDetection.py numberplate5.png")

def task6():
    os.system("python CS373LicensePlateDetection.py numberplate6.png")

def task7():
    os.system("python CS373LicensePlateDetection.py numberplate7.png")

def task8():
    os.system("python CS373LicensePlateDetection.py numberplate8.png")

def task9():
    os.system("python CS373LicensePlateDetection.py numberplate9.png") 

t1 = Thread(target=task1)
t2 = Thread(target=task2)
t3 = Thread(target=task3)
t4 = Thread(target=task4)
t5 = Thread(target=task5)
t6 = Thread(target=task6)
t7 = Thread(target=task7)
t8 = Thread(target=task8)
t9 = Thread(target=task9)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()

# 6 and 1.5 good ratios