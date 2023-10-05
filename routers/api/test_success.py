from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()

@router.post('/api/test-success')
async def test_post(
    request:Request
):
    form = await request.form()

    return (
        {
            'result':form
        }
    )