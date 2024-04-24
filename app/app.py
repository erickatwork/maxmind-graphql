# app.py
from starlette.applications import Starlette
from starlette.routing import Route
from strawberry.asgi import GraphQL
from schema import schema

graphql_app = GraphQL(schema)

app = Starlette(debug=True, routes=[
    Route("/graphql", graphql_app, methods=["GET", "POST"]),
])
