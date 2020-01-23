class Employee:
    def __init__(self, FirstName, LastName):
        self.FirstName = FirstName
        self.LastName = LastName

EmployeeDictionary  = {
    "Bryan" : "Fassett",
    "Kelly" : "Holllis"
}

for employee in EmployeeDictionary:
    MyEmployee = Employee(EmployeeDictionary[employee])
    print(f"{MyEmployee.FirstName} {MyEmployee.LastName}")