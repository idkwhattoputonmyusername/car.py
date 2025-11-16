import pandas as pd
import os

CAR_DATA_FILE = "cars.csv"
PRICE_DEFAULT = 1000

class Customer:
    def __init__(self, customer_id, name, contact_info):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Клієнт ID: {self.customer_id} Ім'я: {self.name} Контакти: {self.contact_info}"


class RentalAgreement:
    def __init__(self, agreement_id, car_details, customer, start_date, end_date, rental_days):
        self.agreement_id = agreement_id
        self.car_details = car_details
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date
        self.rental_days = rental_days
        self.rental_price_per_day = car_details.get('price', PRICE_DEFAULT)
        self.total_cost = self.calculate_total_cost()

    def calculate_total_cost(self):
        cost = self.rental_price_per_day * self.rental_days
        return cost

    def generate_confirmation(self):
        print("\nПідтвердження Прокату (Договір)")
        print(f"Договір №: {self.agreement_id}")
        print(f"Клієнт: {self.customer.name} (ID: {self.customer.customer_id})")
        print(f"Автомобіль ID: {self.car_details['id']} | {self.car_details['make']} {self.car_details['model']} ({self.car_details['year']})")
        print(f"Дати оренди: з {self.start_date} до {self.end_date}")
        print(f"Кількість днів: {self.rental_days}")
        print(f"Ціна за день: {self.rental_price_per_day} UAH")
        print(f"Загальна вартість: {self.total_cost} UAH")

    def __str__(self):
        return f"Договір №{self.agreement_id} ({self.customer.name} орендує {self.car_details['make']} {self.car_details['model']})"

class RentalAgency:
    def __init__(self, car_file):
        self.customers = {}
        self.agreements = {}
        self.next_agreement_id = 1001
        self.car_file = car_file
        self.cars_df = self._load_car_data()
        
        print("Система Прокату Автомобілів ініціалізована.")
        print(f"Завантажено {len(self.cars_df)} автомобілів з {self.car_file}.")

    def _load_car_data(self):
        try:
            df = pd.read_csv(
                self.car_file, 
                sep=',', 
                dtype={'id': str, 'make': str, 'model': str, 'year': int, 'available': str}
            )
            df['available_bool'] = df['available'].str.lower().map({'yes': True, 'no': False})
            
            if 'price' not in df.columns:
                 df['price'] = PRICE_DEFAULT 
            
            df.set_index('id', inplace=True)
            return df
        except FileNotFoundError:
            print(f"ПОМИЛКА: Файл даних {self.car_file} не знайдено.")
            return pd.DataFrame()
        except Exception as e:
             print(f"ПОМИЛКА при читанні CSV: {e}")
             return pd.DataFrame()

    def _save_car_data(self):
        df_to_save = self.cars_df.copy()
        df_to_save['available'] = df_to_save['available_bool'].map({True: 'yes', False: 'no'})
        df_to_save.reset_index(inplace=True) # Повертаємо 'id' як звичайний стовпець
        df_to_save.to_csv(self.car_file, index=False, columns=['id', 'make', 'model', 'year', 'available', 'price']) # Зберігаємо лише потрібні колонки
        
    def register_customer(self, customer):
        self.customers[customer.customer_id] = customer

    def get_available_cars(self):
        available_cars_df = self.cars_df[self.cars_df['available_bool'] == True]
        
        print("\n=== Доступні Автомобілі ===")
        if available_cars_df.empty:
            print("Наразі немає доступних автомобілів.")
        else:
            for car_id, car in available_cars_df.iterrows():
                 print(f"ID: {car_id} Авто: {car['make']} {car['model']} ({car['year']}) Ціна/день: {car['price']} UAH Статус: Доступний")

        return available_cars_df

    def rent_car(self, customer_id, car_id, start_date, end_date, rental_days):
        
        if car_id not in self.cars_df.index:
            print(f"\nПОМИЛКА: Автомобіль ID {car_id} не існує.")
            return None
            
        car_row = self.cars_df.loc[car_id]
        
        if not car_row['available_bool']:
            print(f"\nПОМИЛКА: Автомобіль ID {car_id} вже заброньований.")
            return None

        if customer_id not in self.customers:
            print(f"\nПОМИЛКА: Клієнт ID {customer_id} не знайдений.")
            return None

        customer = self.customers[customer_id]

        agreement = RentalAgreement(
            self.next_agreement_id, car_row, customer, start_date, end_date, rental_days
        )
        self.cars_df.loc[car_id, 'available_bool'] = False
        self._save_car_data() 
        
        self.agreements[agreement.agreement_id] = agreement
        self.next_agreement_id += 1

        print(f"\nУСПІХ: Автомобіль {car_id} видано. Створено договір №{agreement.agreement_id}.")
        agreement.generate_confirmation()
        
        return agreement

    def return_car(self, agreement_id):
        if agreement_id not in self.agreements:
            print(f"\nПОМИЛКА: Договір №{agreement_id} не знайдено.")
            return

        agreement = self.agreements[agreement_id]
        car_id = agreement.car_details.name

        if car_id in self.cars_df.index:
             self.cars_df.loc[car_id, 'available_bool'] = True
             self._save_car_data()

             print(f"\nПОВЕРНЕННЯ: Автомобіль {car_id} ({agreement.car_details['make']} {agreement.car_details['model']}) успішно повернено.")
        else:
             print(f"\nПОПЕРЕДЖЕННЯ: Автомобіль ID {car_id} не знайдено в базі даних, але договір завершено.")

        del self.agreements[agreement_id]
        print(f"Договір №{agreement_id} завершено.")

agency = RentalAgency(CAR_DATA_FILE)

customer1 = Customer(customer_id="P101", name="Іван Сидоренко", contact_info="ivan@example.com")
customer2 = Customer(customer_id="P102", name="Олена Петренко", contact_info="olena@example.com")

agency.register_customer(customer1)
agency.register_customer(customer2)

print("\nЕТАП 1: Клієнт переглядає доступні авто (з cars.csv)")
available_cars = agency.get_available_cars()


print("\nЕТАП 2: Клієнт бронює авто '234' (Toyota Camry)")
rental_days = 5
agreement_ivan = agency.rent_car(
    customer_id="P101", 
    car_id="234", 
    start_date="2025-11-15", 
    end_date="2025-11-20", 
    rental_days=rental_days
)

print(f"\nПеревірка статусу '234' після бронювання: Доступний? {agency.cars_df.loc['234', 'available_bool']}")


print("\nЕТАП 3: Спроба забронювати '234' знову")
agency.rent_car(
    customer_id="P102", 
    car_id="234", 
    start_date="2025-11-21", 
    end_date="2025-11-23", 
    rental_days=2
)


if agreement_ivan:
    print(f"\nЕТАП 4: Клієнт {customer1.name} повертає авто")
    agency.return_car(agreement_ivan.agreement_id)

print(f"\nПеревірка статусу '234' після повернення: Доступний? {agency.cars_df.loc['234', 'available_bool']}")

print("\nФінальний перегляд доступних авто")
agency.get_available_cars()
