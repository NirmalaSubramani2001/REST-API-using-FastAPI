from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Employee Management API")

# ---------------------
# Data Model
# ---------------------
class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

# In-memory storage
employees: List[Employee] = []

# ---------------------
# Create Employee
# ---------------------
@app.post("/employees", response_model=Employee)
def create_employee(employee: Employee):
    for emp in employees:
        if emp.id == employee.id:
            raise HTTPException(status_code=400, detail="Employee ID already exists")
    employees.append(employee)
    return employee

# ---------------------
# Get All Employees
# ---------------------
@app.get("/employees", response_model=List[Employee])
def get_employees():
    return employees

# ---------------------
# Get Employee by ID
# ---------------------
@app.get("/employees/{emp_id}", response_model=Employee)
def get_employee(emp_id: int):
    for emp in employees:
        if emp.id == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

# ---------------------
# Update Employee
# ---------------------
@app.put("/employees/{emp_id}", response_model=Employee)
def update_employee(emp_id: int, updated_employee: Employee):
    for index, emp in enumerate(employees):
        if emp.id == emp_id:
            employees[index] = updated_employee
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found")

# ---------------------
# Delete Employee
# ---------------------
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    for emp in employees:
        if emp.id == emp_id:
            employees.remove(emp)
            return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")
