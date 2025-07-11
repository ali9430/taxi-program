"""Simple Taxi App CLI
This script provides a minimal in-memory taxi dispatch system.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import math

@dataclass
class Rider:
    id: int
    name: str

@dataclass
class Driver:
    id: int
    name: str
    x: float
    y: float
    available: bool = True

@dataclass
class Ride:
    id: int
    rider: Rider
    driver: Driver
    start_x: float
    start_y: float
    dest_x: float
    dest_y: float
    fare: float
    completed: bool = False

class TaxiApp:
    """Core application state and logic."""

    def __init__(self):
        self.riders: Dict[int, Rider] = {}
        self.drivers: Dict[int, Driver] = {}
        self.rides: Dict[int, Ride] = {}
        self._rider_id = 1
        self._driver_id = 1
        self._ride_id = 1

    def register_rider(self, name: str) -> Rider:
        rider = Rider(id=self._rider_id, name=name)
        self.riders[self._rider_id] = rider
        self._rider_id += 1
        print(f"Registered rider {rider.name} with ID {rider.id}")
        return rider

    def register_driver(self, name: str, x: float, y: float) -> Driver:
        driver = Driver(id=self._driver_id, name=name, x=x, y=y)
        self.drivers[self._driver_id] = driver
        self._driver_id += 1
        print(f"Registered driver {driver.name} with ID {driver.id} at location ({x}, {y})")
        return driver

    def _find_closest_driver(self, x: float, y: float) -> Optional[Driver]:
        closest = None
        closest_dist = float('inf')
        for driver in self.drivers.values():
            if not driver.available:
                continue
            dist = math.hypot(driver.x - x, driver.y - y)
            if dist < closest_dist:
                closest = driver
                closest_dist = dist
        return closest

    def request_ride(self, rider_id: int, start_x: float, start_y: float, dest_x: float, dest_y: float) -> Optional[Ride]:
        rider = self.riders.get(rider_id)
        if not rider:
            print("Rider not found")
            return None
        driver = self._find_closest_driver(start_x, start_y)
        if not driver:
            print("No available drivers")
            return None
        driver.available = False
        distance = math.hypot(dest_x - start_x, dest_y - start_y)
        fare = round(250 + distance * 100, 2)  # base fare plus per km
        ride = Ride(id=self._ride_id, rider=rider, driver=driver,
                    start_x=start_x, start_y=start_y, dest_x=dest_x, dest_y=dest_y, fare=fare)
        self.rides[self._ride_id] = ride
        self._ride_id += 1
        print(f"Ride {ride.id} started with driver {driver.name}. Fare will be {fare}")
        return ride

    def complete_ride(self, ride_id: int) -> None:
        ride = self.rides.get(ride_id)
        if not ride:
            print("Ride not found")
            return
        if ride.completed:
            print("Ride already completed")
            return
        ride.completed = True
        ride.driver.available = True
        ride.driver.x = ride.dest_x
        ride.driver.y = ride.dest_y
        print(f"Ride {ride.id} completed. Fare was {ride.fare}")

    def list_rides(self) -> None:
        for ride in self.rides.values():
            status = "completed" if ride.completed else "active"
            print(f"Ride {ride.id} ({status}): Rider {ride.rider.name} -> Driver {ride.driver.name}")


def main():
    app = TaxiApp()
    while True:
        print("\n--- Taxi App ---")
        print("1. Register rider")
        print("2. Register driver")
        print("3. Request ride")
        print("4. Complete ride")
        print("5. List rides")
        print("6. Quit")
        choice = input("Choose an option: ")
        if choice == '1':
            name = input("Rider name: ")
            app.register_rider(name)
        elif choice == '2':
            name = input("Driver name: ")
            x = float(input("Driver start X: "))
            y = float(input("Driver start Y: "))
            app.register_driver(name, x, y)
        elif choice == '3':
            rider_id = int(input("Rider ID: "))
            sx = float(input("Start X: "))
            sy = float(input("Start Y: "))
            dx = float(input("Destination X: "))
            dy = float(input("Destination Y: "))
            app.request_ride(rider_id, sx, sy, dx, dy)
        elif choice == '4':
            ride_id = int(input("Ride ID: "))
            app.complete_ride(ride_id)
        elif choice == '5':
            app.list_rides()
        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
