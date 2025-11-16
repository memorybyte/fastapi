import json
from typing import List, Dict, Optional, Annotated, Literal
from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str,
                  Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str,
                    Field(..., description='City where the patient is living')]
    age: Annotated[int,
                   Field(..., description='Age of the patient', gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'],
                      Field(..., description='Gender of the patient')]
    height: Annotated[float,
                      Field(..., description='Height of the patient',  gt=0)]
    weight: Annotated[float,
                      Field(..., description='Weight of the patient',  gt=0)]

    @computed_field()
    @property
    def bmi(self) -> float:
        return round((self.weight / (self.height ** 2)), 2)

    @computed_field()
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'nomarl'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male',
                                       'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get('/')
def home():
    return {'message': 'Patient Management System API'}


@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}


@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(
        patient_id: str = Path(
            ...,  # Three dots indicate that the path parameter is required.k
            description='ID of the patient in th DB',
            example='P001',
        )):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    # return {'error': 'Patient not found'}
    raise HTTPException(
        status_code=404,
        detail='Patient not found'
    )


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(...,
                         description='Sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='Sort in asc or desc order')
):

    valid_field = ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid field. Select from {valid_field}'
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid order. Select between asc and desc'
        )

    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(
        sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):
    # The data patient is already validated by FastAPI

    # Load the data
    data = load_data()

    # Check if patient exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # Add new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    patient = data[patient_id]
    patient_dict = patient_update.model_dump(exclude_unset=True)

    # for field in patient_dict:
    #     if field:
    #         patient[field] = patient_dict[field]

    for key, value in patient_dict.items():
        patient[key] = value

    patient['id'] = patient_id
    patient = Patient(**patient)
    patient = patient.model_dump(exclude=['id'])

    data[patient_id] = patient
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient details updated successfully'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail={
                            'message': 'Patient does not exist'})

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted'})
