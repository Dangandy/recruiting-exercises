#!/usr/bin/python


import unittest
from inventory_allocator import InventoryAllocator


class InventoryAllocatorTest(unittest.TestCase):

    # test function 1: getFurthestWarehouse
    def testGetFurthestWarehouseNotFound(self):
        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 0}}]
        inventoryAllocator = InventoryAllocator()
        furthest = inventoryAllocator.getFurthestWarehouse(orders, warehouses)
        self.assertEqual(furthest, -1)

    def testGetFurthestWarehouseOneOrder(self):
        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        inventoryAllocator = InventoryAllocator()
        furthest = inventoryAllocator.getFurthestWarehouse(orders,
                warehouses)
        self.assertEqual(furthest, 0)

    def testGetFurthestWarehouseManyOrder(self):
        orders = {'apple': 5, 'banana': 5, 'orange': 5}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5,
                      'orange': 10}}, {'name': 'dm',
                      'inventory': {'banana': 5, 'orange': 10}}]
        inventoryAllocator = InventoryAllocator()
        furthest = inventoryAllocator.getFurthestWarehouse(orders, warehouses)
        self.assertEqual(furthest, 1)

    def testGetFurthestWarehouseLeftoverOrder(self):
        orders = {'apple': 5, 'banana': 5, 'orange': 5}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5, 'orange': 10}},
                      {'name': 'dm', 'inventory': {'banana': 5, 'orange': 10}}]
        inventoryAllocator = InventoryAllocator()
        furthest = inventoryAllocator.getFurthestWarehouse(orders, warehouses)
        self.assertEqual(furthest, 1)

    # This test case failed while testing other function
    def testGetFurthestWarehouseChooseClosest(self):
        orders = {'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5, 'orange': 10}},
                      {'name': 'dm', 'inventory': {'apple': 5, 'orange': 10}}]
        furthest = 0
        inventoryAllocator = InventoryAllocator()
        furthest = inventoryAllocator.getFurthestWarehouse(orders, warehouses)
        self.assertEqual(furthest, 0)

    # test function 2: emptyWarehouse
    # warehouse will always contain order, as it is checked before running
    def testEmptyWarehouseOneOrder(self):
        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        furthest = 0
        cheapestShipment = []
        inventoryAllocator = InventoryAllocator()
        leftovers, cheapestShipment = \
            inventoryAllocator.emptyWarehouse(orders,
                                              warehouses,
                                              furthest,
                                              cheapestShipment)
        self.assertEqual(leftovers, {'apple': 0})
        self.assertEqual(cheapestShipment, [{'owd': {'apple': 1}}])

    def testEmptyWarehouseOneOrderWithLeftovers(self):
        orders = {'orange': 20}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5, 'orange': 10}},
                      {'name': 'dm', 'inventory': {'banana': 5, 'orange': 10}}]
        furthest = 1
        cheapestShipment = []
        inventoryAllocator = InventoryAllocator()
        leftovers, cheapestShipment = \
            inventoryAllocator.emptyWarehouse(orders,
                                              warehouses,
                                              furthest,
                                              cheapestShipment)
        self.assertEqual(leftovers, {'orange': 10})
        self.assertEqual(cheapestShipment, [{'dm': {'orange': 10}}])

    def testEmptyWarehouseManyOrder(self):
        orders = {'banana': 5, 'orange': 5}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5, 'orange': 10}},
                      {'name': 'dm', 'inventory': {'banana': 5, 'orange': 10}}]
        furthest = 1
        cheapestShipment = []
        inventoryAllocator = InventoryAllocator()
        (leftovers, cheapestShipment) = \
            inventoryAllocator.emptyWarehouse(orders,
                                              warehouses,
                                              furthest,
                                              cheapestShipment)
        self.assertEqual(leftovers, {'banana': 0, 'orange': 0})
        self.assertEqual(cheapestShipment, [{'dm': {'banana': 5, 'orange': 5}}])

    def testEmptyWarehouseManyOrderWithLeftovers(self):
        orders = {'banana': 5, 'orange': 5, 'apple': 5}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5, 'orange': 10}},
                      {'name': 'dm', 'inventory': {'banana': 5, 'orange': 10}}]
        furthest = 1
        cheapestShipment = []
        inventoryAllocator = InventoryAllocator()
        leftovers, cheapestShipment = \
            inventoryAllocator.emptyWarehouse(orders,
                                              warehouses,
                                              furthest,
                                              cheapestShipment)
        self.assertEqual(leftovers, {'banana': 0, 'orange': 0, 'apple': 5})
        self.assertEqual(cheapestShipment, [{'dm': {'banana': 5, 'orange': 5}}])

    # test function 3: getCheapestShipments
    def testGetCheapestShipmentsNotFound(self):
        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 0}}]
        inventoryAllocator = InventoryAllocator()
        cheapestShipment = \
            inventoryAllocator.getCheapestShipments(orders, warehouses)
        self.assertEqual(cheapestShipment, [])

    def testGetCheapestShipmentsOneOrder(self):
        orders = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        inventoryAllocator = InventoryAllocator()
        cheapestShipment = \
            inventoryAllocator.getCheapestShipments(orders, warehouses)
        self.assertEqual(cheapestShipment, [{'owd': {'apple': 1}}])

    def testGetCheapestShipmentsOneOrderMultipleShipments(self):
        orders = {'apple': 10}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                      {'name': 'dm', 'inventory': {'apple': 5}}]
        inventoryAllocator = InventoryAllocator()
        cheapestShipment = \
            inventoryAllocator.getCheapestShipments(orders, warehouses)
        self.assertEqual(cheapestShipment, [{'dm': {'apple': 5}},
                                            {'owd': {'apple': 5}}])

    def testGetCheapestShipmentsMultipleOrderOneShipment(self):
        orders = {
            'apple': 5,
            'orange': 5,
            'banana': 5,
            'grape': 5,
            }
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                      {'name': 'dm', 'inventory': {'orange': 5}},
                      {'name': 'bb', 'inventory': {'banana': 5}},
                      {'name': 'all', 'inventory': {
                                                    'apple': 10,
                                                    'orange': 10,
                                                    'banana': 10,
                                                    'grape': 10,
                                                    }},
                      {'name': 'gg', 'inventory': {'grape': 5}}]
        inventoryAllocator = InventoryAllocator()
        cheapestShipment = \
            inventoryAllocator.getCheapestShipments(orders, warehouses)
        self.assertEqual(cheapestShipment, [{'all': {
            'apple': 5,
            'orange': 5,
            'banana': 5,
            'grape': 5,
            }}])

    def testGetCheapestShipmentsMultipleOrderMultipleShipment(self):
        orders = {
            'apple': 5,
            'orange': 5,
            'banana': 5,
            'grape': 5,
            }
        warehouses = [{'name': 'owd', 'inventory': {'apple': 5}},
                      {'name': 'dm', 'inventory': {'orange': 5}},
                      {'name': 'bb', 'inventory': {'banana': 5}},
                      {'name': 'gg', 'inventory': {'grape': 5}},
                      {'name': 'all', 'inventory': {
                                                    'apple': 10,
                                                    'orange': 10,
                                                    'banana': 10,
                                                    'grape': 10,
                                                    }}]
        inventoryAllocator = InventoryAllocator()
        cheapestShipment = \
            inventoryAllocator.getCheapestShipments(orders, warehouses)
        self.assertEqual(cheapestShipment, [{'gg': {'grape': 5}},
                                            {'bb': {'banana': 5}},
                                            {'dm': {'orange': 5}},
                                            {'owd': {'apple': 5}}])


if __name__ == '__main__':
    unittest.main()
