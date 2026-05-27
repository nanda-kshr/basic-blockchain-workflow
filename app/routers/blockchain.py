from fastapi import APIRouter, Query
from app.schemas.blockchain import DataCreate, DataOut, SearchOut
from app.deps.blackchain_instance import blockchain

router = APIRouter(prefix="/blockchain", tags=["blockchain"])


@router.post("", response_model=DataOut)
async def add_data(
    payload: DataCreate
) -> DataOut:
    try:
        data = payload.data
        blockchain.add_data(data)
    except Exception as e:
        return {"error": str(e)}
    return {"data": "success"}

@router.get("", response_model=SearchOut)
async def get_data(
    index: int = Query(..., ge=1)
) -> SearchOut:
    try:
        mydata = blockchain.get_data(index)
        return {"data": mydata}
    except Exception as e:
        return {"error": str(e)}

