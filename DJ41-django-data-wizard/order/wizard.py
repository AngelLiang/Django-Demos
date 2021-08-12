import data_wizard
from .models import Order

data_wizard.register(Order)
# data_wizard.set_loader(Order, "order.loaders.OrderLoader")
