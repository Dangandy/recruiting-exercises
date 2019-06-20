# Inventory Allocator

Inventory Allocator is a tool that will calculate the best way an order can be shipped given inventory across a set of warehouses.

Note: Algorithm will try to package all items into fewest shipments with cost in mind.

## Usage

Below is a sample usage of InventoryAllocator:

> from inventory_allocator import InventoryAllocator
> orders = { "banana": 5, "orange": 5, "apple": 5}
> warehouses = [{ "name": "owd", "inventory": { "apple": 5, "orange": 10 } }, { "name": "dm", "inventory": { "banana": 5, "orange": 10} }]
> inventoryAllocator = InventoryAllocator()
> cheapestShipment = inventoryAllocator.getCheapestShipments(orders, warehouses)

To view unit tests of InventoryAllocator enter the following command:

> python3 inventory-allocator.test.py
