from sanic import Sanic, Request
from sanic.response import text, json


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from gymapp.models import Subscription, Payment, Client, Base
from pathlib import Path

app = Sanic("MyHelloWorldApp")

db_path = db_path = Path(__file__).parent.parent / "data" / "gym4.db" 
print(db_path)
engine = create_engine(f"sqlite:///{db_path}", echo=False)


@app.get("/clients")
async def get_clients(request: Request):
    with Session(engine) as session:
        clients = Client.all(session=session)
    return json([client.to_dict() for client in clients])


@app.post("/clients")
async def create_client(request: Request):

    payload = request.json
    return json(f"create client payload : {payload}")


@app.get("/clients/<id>")
async def get_client(request: Request, id):
    with Session(engine) as session:
        client = Client.get(session=session, id = id)
    return json(client.to_dict() if client is not None else {'msg':'client doesnt exist'}) # type: ignore


@app.patch("/clients/<id>")
async def patch_client(request: Request, id):
    # TODO patch client od id = <id>
    patch_payload = request.json
    return json({})


@app.delete("/clients/<id>")
async def delete_client(request: Request, id):
    with Session(engine) as session:
        client = Client.get(session=session, id = id)
        client.delete() # type: ignore
    return json({"msg": "deleted"})# ty


# @app.post("/clients")
# async def create_client(request: Request):

#     payload = request.json
#     return json(f"create client payload : {payload}")


# app.add_route(get_hello_world_name, "/<name>", methods=["GET"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, dev=True)
