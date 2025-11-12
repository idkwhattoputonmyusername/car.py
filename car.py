class Car:
    def __init__(self, car_id, make, model, year, price, is_available=True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.rental_price_per_day = price
        self.is_available = is_available
        print(f"Car {self.car_id} ({self.make} {self.model}) створено.")

    def is_available(self):
        return self.is_available

    def set_availability(self, status):
        self.is_available = status

    def __str__(self):
        status = "Доступний" if self.is_available else "Заброньований"
        return f"ID: {self.car_id} Авто: {self.make} {self.model} ({self.year}) Ціна/день: {self.rental_price_per_day} UAH Статус: {status}"


class Customer:
    def __init__(self, customer_id, name, contact_info):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Клієнт ID: {self.customer_id} Ім'я: {self.name} Контакти: {self.contact_info}"


class RentalAgreement:
    def __init__(self, agreement_id, car, customer, start_date, end_date, rental_days):
        self.agreement_id = agreement_id
        self.car = car
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date
        self.rental_days = rental_days
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self):
        cost = self.car.rental_price_per_day * self.rental_days
        return cost

    def generate_confirmation(self):
        print("Підтвердження Прокату (Договір)")
        print(f"Договір №: {self.agreement_id}")
        print(f"Клієнт: {self.customer.name} (ID: {self.customer.customer_id})")
        print(f"Автомобіль: {self.car.make} {self.car.model} (ID: {self.car.car_id})")
        print(f"Дати оренди: з {self.start_date} до {self.end_date}")
        print(f"Кількість днів: {self.rental_days}")
        print(f"Загальна вартість: {self.total_cost} UAH")

    def __str__(self):
        return f"Договір №{self.agreement_id} ({self.customer.name} орендує {self.car.make} {self.car.model})"


class RentalAgency:
    def __init__(self):
        self.cars = {}
        self.customers = {}
        self.agreements = {}
        self.next_agreement_id = 1001
        print("Система Прокату Автомобілів ініціалізована.")

    def add_car(self, car):
        self.cars[car.car_id] = car

    def register_customer(self, customer):
        self.customers[customer.customer_id] = customer

    def get_available_cars(self):
        available = [car for car in self.cars.values() if car.is_available]
        print("\nДоступні Автомобілі")
        if not available:
            print("Наразі немає доступних автомобілів.")
        for car in available:
            print(car)
        return available

    def rent_car(self, customer_id, car_id, start_date, end_date, rental_days):
        if car_id not in self.cars or not self.cars[car_id].is_available:
            print(f"\nПОМИЛКА: Автомобіль ID {car_id} недоступний або не існує.")
            return None

        if customer_id not in self.customers:
            print(f"\nПОМИЛКА: Клієнт ID {customer_id} не знайдений.")
            return None

        car = self.cars[car_id]
        customer = self.customers[customer_id]

        agreement = RentalAgreement(
            self.next_agreement_id, car, customer, start_date, end_date, rental_days
        )

        car.set_availability(False)
        self.agreements[agreement.agreement_id] = agreement

        print(f"\nУСПІХ: Автомобіль {car_id} видано. Створено договір №{agreement.agreement_id}.")
        agreement.generate_confirmation()

        self.next_agreement_id += 1
        return agreement

    def return_car(self, agreement_id):
        if agreement_id not in self.agreements:
            print(f"\nПОМИЛКА: Договір №{agreement_id} не знайдено.")
            return

        agreement = self.agreements[agreement_id]
        car = agreement.car
        
        car.set_availability(True)
        
        print(f"\nПОВЕРНЕННЯ: Автомобіль {car.car_id} ({car.make} {car.model}) успішно повернено.")
        del self.agreements[agreement_id]
        print(f"Договір №{agreement_id} завершено.")


agency = RentalAgency()

car1 = Car(car_id="C001", make="Toyota", model="Camry", year=2020, price=800)
car2 = Car(car_id="C002", make="Honda", model="Civic", year=2022, price=750)
car3 = Car(car_id="C003", make="BMW", model="X5", year=2023, price=1500, is_available=False) # Спочатку недоступний

agency.add_car(car1)
agency.add_car(car2)
agency.add_car(car3)

customer1 = Customer(customer_id="P101", name="Іван Сидоренко", contact_info="ivan@example.com")
customer2 = Customer(customer_id="P102", name="Олена Петренко", contact_info="olena@example.com")

agency.register_customer(customer1)
agency.register_customer(customer2)

print("\nЕТАП 1: Клієнт переглядає доступні авто")
available_cars = agency.get_available_cars()

print("\nЕТАП 2: Клієнт бронює авто C001")
rental_days = 5
agreement_ivan = agency.rent_car(
    customer_id="P101", 
    car_id="C001", 
    start_date="2025-11-15", 
    end_date="2025-11-20", 
    rental_days=rental_days
)

print(f"\nПеревірка статусу C001 після бронювання: Доступний? {car1.is_available}")


print("\nЕТАП 3: Спроба забронювати C001 знову")
agency.rent_car(
    customer_id="P102", 
    car_id="C001", 
    start_date="2025-11-21", 
    end_date="2025-11-23", 
    rental_days=2
)


if agreement_ivan:
    print(f"\nЕТАП 4: Клієнт {customer1.name} повертає авто")
    agency.return_car(agreement_ivan.agreement_id)

print(f"\nПеревірка статусу C001 після повернення: Доступний? {car1.is_available}")

print("\nФінальний перегляд доступних авто")
agency.get_available_cars()