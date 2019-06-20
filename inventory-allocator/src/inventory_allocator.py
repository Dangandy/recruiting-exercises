#!/usr/bin/python


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
                # if remainder >= 0, we get false positive
                # see test: testGetCheapestShipmentsOneOrderMultipleShipments
                while index < len(warehouses) and remainder > 0:
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
        Note: warehouse is modified because
        """

        # variables
        Toggle_First_Add = True

        # empty orders with furthest warehouse
        for key, value in orders.items():
            if value > 0:
                if key in warehouses[furthest]['inventory'].keys():
                    inventory = \
                        min(warehouses[furthest]['inventory'][key], value)
                    orders[key] = value - inventory
                    warehouseName = warehouses[furthest]['name']

                    # add warehouse or update key/value
                    if Toggle_First_Add:
                        cheapestShipment.append({warehouseName : {
                            key : inventory } } )
                        Toggle_First_Add = not Toggle_First_Add
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
                leftovers, cheapestShipment = \
                    self.emptyWarehouse(leftovers,
                                        warehouses,
                                        furthest,
                                        cheapestShipment)
        return cheapestShipment
