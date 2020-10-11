# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 22:19:29 2020

@author: DANQI
"""
# import random

# class Road:
#     def __init__(self,name,length):
#         self.name=name
#         self.len=length

# class Car:
#     def __init__(self,brand,speed):
#         self.brand=brand
#         self.speed=speed
#     def get_time(self,road):
#         ran_time=random.randint(1,10)
#         msg='{}品牌的车在{}上以{}速度行驶{}小时'.format(self.brand,road.name,self.speed,ran_time)
#         print(msg)
#     def __str__(self):
#         return '{}品牌的，速度{}'.format(self.brand,self.speed)

# r=Road('京藏高速',12000)
# audi=Car('奥迪',120)

# print(r.name)

# audi.get_time(r)

class Computer:
    def __init__(self,brand,type,color):
        self.brand=brand
        self.type=type
        self.color=color
    def online(self):
        print("正在使用电脑上网")
    def __str__(self):
        return self.brand +'---'+self.type+'---'+self.color
    
    
class Book:
    def __init__(self,bname,author,number):
        self.bname=bname
        self.author=author
        self.number=number
    def __str__(self):
        return self.bname+"---"+self.author+'---'+str(self.number)

        
class Student:
    def __init__(self,name,computer,book):
        self.name=name
        self.computer=computer
        self.books=[]
        self.books.append(book)
    def borrow_book(self,book):
        for book1 in self.books:
            if book1.bname==book.bname:
                print(book1.bname)
                break
            else:
                self.books.append(book)
                print(book1.bname)
    def show_book(self):
        for book in self.books:
          print(book.bname)
          
    def __str__(self):
        return self.name+'---'+str(self.computer)+'---'+str(self.books)
        

computer=Computer('mac','mac_pro_2018','grey')
book=Book('note','bill',19)

student=Student('haha',computer,book)
print('----------------')
book1=Book('note2','jhon',3)
student.borrow_book(book1)

print('----------------')
student.show_book()

        
        
        
    


    
        
        
            
            
        
        
        
    
    
        
        