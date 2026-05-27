from fastapi import APIRouter
from app.schemas.blockchain import DataCreate, DataOut
from app.deps.blackchain_instance import blockchain

router = APIRouter(prefix="/blockchain", tags=["blockchain"])


@router.post("", response_model=DataOut)
async def create_attendance(
    payload: DataCreate
) -> DataOut:
    try:
        data = payload.data
        blockchain.add_data(data)
    except Exception as e:
        return {"error": str(e)}
    return {"data": "success"}

