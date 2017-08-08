# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 22:49:41 2017

This is a small example of nested classes in Python 3. 
For now the inner class People.Person is visible to code outside of class
People. This is not what we would ideally want. However, it nevertheless demonstrates 
some basic OOP principles.


It demonstrates use of private instance variables (these are prefaced w/ "__", but
NOT succeeded by "__"). People.Person has private instance var __name.
People has private instance variable __ppl. Also note that __ppl in class People IS NOT accessible
via a getter. Rather its elements are accessible via the generator, pplGen.

People has an add method that adds a Person if the person does not already exist in the contained list.
However, by default, Person("p1") and Person("p1") are distinct people; this is overridden
by use of the _eq__ method in class Person.

Also, if class People did not implement the __eq__ method in this way, 
if you have the following sequence, a value error would be raised by the the
call to __ppl.remove() in People.remove():
>>> ppl = People()
>>> ppl.add("p1")
>>> ppl.remove("p1")
The error would be raised because ppl.add("p1") would cause Person("p1")
to be added to the list contained in the People instance, ppl. 
However, ppl.remove("p1") would cause Person("p1") to be constructed, 
and this is a distinct person instance from the one added- so
as far as ppl.__ppl.remove(Person("p1")) is concerned, the element
passed to ppl.__ppl.remove() isn't present in the list. Overridding
of the __eq__ method in class Person helps us circumvent this issue.

"""

class People(object):
    class Person(object):
        def __init__(self,name):
            self.__name=name
        def __str__(self):
            return self.__name
        
        def __eq__(self, other):
            if not isinstance(other, People.Person): #People.Person accesses outer class
                return False
            return self.__name==other.__name
            
    def __init__(self):
        self.__ppl=[]
        
    def add(self, person):
        if not isinstance(person, str):
            raise TypeError("param must be of type str")
        person = self.Person(person)
        if not person in self.__ppl:
            self.__ppl.append(person)
    
    
    def remove(self, person):
        thePerson = self.Person(person)
        try:
            self.__ppl.remove(thePerson)
        except ValueError:
            print("Element "+person+" not in collection")
            
    def pplGen(self):
        for person in self.__ppl:
            yield person
    
ppl = People()
ppl.add("person 1")
ppl.add("person 2")
group = ppl.pplGen()
for e in group:
    print(e, type(e))


ppl.remove("person 1")
group = ppl.pplGen()
for e in group:
    print(e)

print("TRYING TO ADD ELEMENT THAT'S ALREADY PRESENT")
ppl.add("person 2")

group = ppl.pplGen()
for e in group:
    print(e)

bad_practice=People.Person("This works, but really shouldn't")
print(bad_practice)    
