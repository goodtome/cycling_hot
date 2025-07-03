from fastapi import FastAPI
from app.api import history

app = FastAPI(title="Cycling App API")

# 路由注册（后续可补充具体实现）
# from app.api import brands, history, events, models, riders, teams, users
# app.include_router(brands.router, prefix="/brands", tags=["品牌"])
app.include_router(history.router, prefix="/history", tags=["历史"])
# app.include_router(events.router, prefix="/events", tags=["赛事"])
# app.include_router(models.router, prefix="/models", tags=["车型"])
# app.include_router(riders.router, prefix="/riders", tags=["车手"])
# app.include_router(teams.router, prefix="/teams", tags=["车队"])
# app.include_router(users.router, prefix="/users", tags=["用户"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Cycling App API!"} 