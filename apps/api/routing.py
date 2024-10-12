from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from .views.users.handlers import router as users_router
from .views.transactions.handlers import router as transactions_router

api = NinjaAPI()

api.add_router('/users/', users_router)
api.add_router('/transactions/', transactions_router)
api.add_router('/auth/', obtain_pair_router)
