from models import Employee
from typing import List
from fastapi import FastAPI, HTTPException, Path, Query

employees_db: List[Employee] = []

app = FastAPI()


@app.get('/')
def home():
    return {'message': 'Hello FastAPI!!!'}


@app.get('/employees', response_model=List[Employee])
def get_employees():
    return employees_db


@app.get('/employee/{id}', response_model=Employee)
def get_employee(id: int):
    for employee in employees_db:
        if id == employee.id:
            return employee

    raise HTTPException(
        status_code=404,
        detail={'message': 'Employee not found'}
    )


@app.post('/employees', response_model=Employee)
def add_employee(new_employee: Employee):
    for employee in employees_db:
        if employee.id == new_employee.id:
            raise HTTPException(
                status_code=400,
                detail={'message': 'Employee already exists'}
            )

    employees_db.append(new_employee)

    return new_employee


@app.put('/update_employee/{id}', response_model=Employee)
def update_employee(id: int, update_employee: Employee):
    for index, employee in enumerate(employees_db):
        if update_employee.id == id:
            employees_db[index] = update_employee
            return update_employee

    raise HTTPException(
        status_code=404,
        detail={'message': 'Employee does not exist'}
    )


@app.delete('/delete_employee/{id}')
def delete_employee(id: int):
    for index, employee in enumerate(employees_db):
        if employee.id == id:
            del employees_db[index]
            return {'message': 'Employee deleted'}

    raise HTTPException(
        status_code=404,
        detail={'message': 'Employee does not exist'}
    )
