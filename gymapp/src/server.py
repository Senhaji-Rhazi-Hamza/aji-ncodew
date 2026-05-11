from sanic import Sanic, Request
from sanic.response import text, json

from sanic.exceptions import NotFound


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


@app.delete("/clients/<id>")
async def delete_client(request: Request, id):
    with Session(engine) as session:
        client = Client.get(session=session, id=id)
        client.delete()  # type: ignore
    return json({"msg": "deleted"})  # ty


@app.get("/clients/<id>")
async def get_client(request: Request, id):
    with Session(engine) as session:
        client = Client.get(session=session, id=id)
    return json(client.to_dict() if client is not None else {"msg": "client doesnt exist"})  # type: ignore


@app.post("/clients")
async def create_client(request: Request):
    with Session(engine) as session:
        client = Client.create(session=session, **request.json)

    return json(client.to_dict())


@app.patch("/clients/<id>")
async def update_client(request: Request, id):
    with Session(engine) as session:
        client = Client.get(session=session, id=id)
        if client is None:
            raise NotFound("client doesnt exist")
        client.update(**request.json)
        return json(client.to_dict())


@app.get("/subscriptions")
async def get_subscriptions(request: Request):
    with Session(engine) as session:
        subscriptions = Subscription.all(session=session)
    return json([subscription.to_dict() for subscription in subscriptions])


@app.delete("/subscriptions/<id>")
async def delete_subscription(request: Request, id):
    with Session(engine) as session:
        subscription = Subscription.get(session=session, id=id)
        if subscription is None:
            raise NotFound("subscription doesnt exist")
        subscription.delete()
    return json({"msg": "deleted"})


@app.get("/subscriptions/<id>")
async def get_subscription(request: Request, id):
    with Session(engine) as session:
        subscription = Subscription.get(session=session, id=id)
    return json(subscription.to_dict() if subscription is not None else {"msg": "subscription doesnt exist"})  # type: ignore


@app.post("/subscriptions")
async def create_subscription(request: Request):
    with Session(engine) as session:
        subscription = Subscription.create(session=session, **request.json)

    return json(subscription.to_dict())


@app.patch("/subscriptions/<id>")
async def update_subscription(request: Request, id):
    with Session(engine) as session:
        subscription = Subscription.get(session=session, id=id)
        if subscription is None:
            raise NotFound("subscription doesnt exist")
        subscription.update(**request.json)
        return json(subscription.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, dev=True)
