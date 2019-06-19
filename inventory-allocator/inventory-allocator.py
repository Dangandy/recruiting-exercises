class InventoryAllocator:

    def getFurthestWarehouse(self, orders, warehouses):
        """
        Helper function that finds the last warehouse a driver has to visit
        ( dict, list(dict) ) => int
        """

        # variables
        furthest = 0

        # find furthest warehouse
        for key, value in orders.items():
            if value > 0:
                remainder = value
                index = 0
                while index < len(warehouses) and remainder >= 0:
                    if key in warehouses[index]['inventory'].keys():
                        remainder -= warehouses[index]['inventory'][key]
                        if remainder <= 0:
                            furthest = max(furthest, index)
                    index += 1

                # not enough inventory
                if remainder > 0:
                    return -1

        return furthest

    def emptyWarehouse(self, orders, warehouses, furthest, cheapestShipment):
        """
        Empty the furthest warehouse and return the updated cheapest shipment
        ( dict, list(dict), int, list) => list(dict, list)
        """

        # variables
        Toggle_Add = True

        # empty orders with furthest warehouse
        for key, value in orders.items():
            if value > 0:
                if key in warehouses[furthest]['inventory'].keys():
                    inventory = min(warehouses[furthest]['inventory'][key], value)
                    orders[key] = value - inventory
                    warehouseName = warehouses[furthest]['name']

                    # add warehouse or update key/value
                    if Toggle_Add:
                        cheapestShipment.append({warehouseName : {
                            key : inventory } } )
                        Toggle_Add = not Toggle_Add
                    else:
                        # add onto
                        cheapestShipment[-1][warehouseName][key] = inventory

        return [orders, cheapestShipment]

    def getCheapestShipments(self, orders, warehouses):
        """
        Find the cheapest route a driver should take to fulfill an order

        ( dict, list(dict) ) => list(dict)

        Algorithm:
        1. find the furthest warehouse
        2. empty orders with furthest warehouse
        3. repeat with leftovers
        """

        # variables
        cheapestShipment = []
        leftovers = {}

        # make a deepcopy of orders
        for key, value in orders.items():
            leftovers[key] = value

        # keep finding the furthest warehouse and empty it
        while sum(leftovers.values()) > 0:
            furthest = self.getFurthestWarehouse(leftovers, warehouses)
            if furthest == -1:
                return cheapestShipment
            else:
                leftovers, cheapestShipment = self.emptyWarehouse(leftovers,
                                                                  warehouses,
                                                                  furthest,
                                                                  cheapestShipment)
        return cheapestShipment


# Accept Arguments / Debug
if __name__ == "__main__":
    orders = { "apple": 5, "banana": 5, "orange": 5 }
    warehouse = [{ "name": "owd", "inventory": { "apple": 5, "orange": 10 } }, { "name": "dm", "inventory": { "banana": 5, "orange": 10}}]
    inventoryAllocator = InventoryAllocator()
    print(inventoryAllocator.getCheapestShipments(orders, warehouse))
