import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

import exceptions as exc


async def middleware(request: Request, call_next):
    try:
        data = await call_next(request)
    except exc.NotFound as e:
        print(e)
        data = JSONResponse(status_code=404, content={'error': e.__class__.__name__})
    except exc.IllegalInput as e:
        print(e)
        data = JSONResponse(status_code=422, content={'error': e.__class__.__name__})
    except exc.NoPermission as e:
        print(e)
        data = JSONResponse(status_code=401, content={'error': e.__class__.__name__})
    except Exception as e:
        print(e)
        traceback.print_exc()
        data = JSONResponse(status_code=500, content={'error': e.__class__.__name__})
    return data
