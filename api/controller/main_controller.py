from fastapi import APIRouter, Path
from api.database.database import get_by_date, get_measurements, add_measurement
router = APIRouter()

@router.get('/getdata/{date}')
def getdata(date):
  return get_by_date(date)

@router.get('/getmeasurements')
async def get_all():
  return await get_measurements()

@router.post('/add_measurement')
async def add_measurement_route(temperature: float, humidity: float):
  await add_measurement(temperature=temperature, humidity=humidity)
  return '{"status": 200, "message":"measurement added!"}'
