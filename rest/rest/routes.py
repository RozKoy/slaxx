def includeme(config):
    config.add_route("home", "/")
    config.add_route("order", "api/order{action:.*}")
    config.add_route("orderlist", "api/orderlist{action:.*}")
    config.add_route("product", "api/product{action:.*}")
    config.add_route("user", "api/user{action:.*}")
