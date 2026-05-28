from fastapi import APIRouter, HTTPException, Query
from app.schemas.blockchain import BlockCreate, DataCreate, DataOut, InfoOut, SearchOut
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
        raise HTTPException(status_code=400, detail=str(e))
    return {"data": "success"}

@router.get("", response_model=SearchOut)
async def get_data(
    index: int = Query(..., ge=1)
) -> SearchOut:
    try:
        mydata = blockchain.get_data(index)
        return {"data": mydata}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/block/latest", response_model=BlockCreate)
async def get_latest_block() -> BlockCreate:
    try:
        latest_block = blockchain.get_latest_block()
        return latest_block.to_dict() if latest_block else {"hash_value": "", "timestamp": "", "data": {}, "previous_hash": "", "index": 0}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/info", response_model=InfoOut)
async def get_info() -> InfoOut:
    try:
        info = blockchain.get_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/block", response_model=SearchOut)
async def add_block(payload: BlockCreate) -> SearchOut:
    try:
        block = payload.model_dump()
        blockchain.add_block(block)
        return {"data": block}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/chain", response_model=list[BlockCreate])
async def get_chain() -> list[BlockCreate]:
    try:
        chain = blockchain.chain
        return [block.to_dict() for block in chain]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))