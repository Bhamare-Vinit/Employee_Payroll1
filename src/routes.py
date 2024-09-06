from fastapi import APIRouter ,HTTPException,status,Depends
from .schemas import Employee,UpdateEmployee
from fastapi import Request
from pymongo.collection import Collection
router=APIRouter()

@router.get("/")
def index():
    return {"message": "Hello World"}

def get_employee_collection(request: Request) -> Collection:
    return request.app.collection

@router.post("/employee", status_code=status.HTTP_201_CREATED, response_model=Employee)
async def create_employee(employee: Employee, collection: Collection = Depends(get_employee_collection)):
    if collection.find_one({"id": employee.id}):
        raise HTTPException(status_code=400, detail="Employee with this ID already exists.")
    collection.insert_one(employee.model_dump())  
    return employee
       
@router.get("/employee")
async def get_employees(collection: Collection = Depends(get_employee_collection)):
    employees = list(collection.find({}, {"_id": 0}))
    return {"employees": employees}

@router.get("/employees/{id}")
async def get_employee(id: int, collection: Collection = Depends(get_employee_collection)):
    employee = collection.find_one({"id": id}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{id}")
async def update_employee(id: int, update_data: UpdateEmployee, collection: Collection = Depends(get_employee_collection)):
    existing_employee = collection.find_one({"id": id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    update_data = {k: v for k, v in update_data.model_dump().items() if v is not None}
    collection.update_one({"id": id}, {"$set": update_data})
    return {"message": "Employee updated successfully"}

@router.delete("/employees/{id}", status_code=status.HTTP_200_OK)
async def delete_employee(id: int, collection: Collection = Depends(get_employee_collection)):
    result = collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}