from enum import Enum


class TourType(Enum):
    BEACH = "Пляжний"
    EXCURSION = "Екскурсійний"
    ADVENTURE = "Пригодницький"


class BookingStatus(Enum):
    PENDING = "Очікує"
    CONFIRMED = "Підтверджено"
    CANCELLED = "Скасовано"


class Tour:
    def __init__(self, name, destination, price, duration, tour_type):
        if price <= 0:
            raise ValueError("Ціна повинна бути більше 0")

        if duration <= 0:
            raise ValueError("Тривалість повинна бути більше 0")

        self.name = name
        self.destination = destination
        self._price = price
        self.duration = duration
        self.tour_type = tour_type

    def calculate_price(self):
        return self._price

    def get_info(self):
        return (
            f"{self.name} | "
            f"{self.destination} | "
            f"{self.tour_type.value} | "
            f"{self.calculate_price():.2f} грн | "
            f"{self.duration} днів"
        )


class BeachTour(Tour):
    def __init__(self, name, destination, price, duration):
        super().__init__(
            name,
            destination,
            price,
            duration,
            TourType.BEACH
        )

    def calculate_price(self):
        return self._price * 1.10


class ExcursionTour(Tour):
    def __init__(self, name, destination, price, duration):
        super().__init__(
            name,
            destination,
            price,
            duration,
            TourType.EXCURSION
        )

    def calculate_price(self):
        return self._price * 1.05


class AdventureTour(Tour):
    def __init__(self, name, destination, price, duration):
        super().__init__(
            name,
            destination,
            price,
            duration,
            TourType.ADVENTURE
        )

    def calculate_price(self):
        return self._price * 1.20


class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


class Booking:
    def __init__(self, customer, tour, tourists):
        if tourists <= 0:
            raise ValueError(
                "Кількість туристів повинна бути більше 0"
            )

        self.customer = customer
        self.tour = tour
        self.tourists = tourists
        self.status = BookingStatus.PENDING

    def confirm(self):
        self.status = BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CANCELLED

    def total_price(self):
        return self.tour.calculate_price() * self.tourists

    def get_info(self):
        return (
            f"Клієнт: {self.customer.name}\n"
            f"Тур: {self.tour.name}\n"
            f"Кількість туристів: {self.tourists}\n"
            f"Загальна вартість: "
            f"{self.total_price():.2f} грн\n"
            f"Статус: {self.status.value}"
        )


class TourManager:
    def __init__(self):
        self.tours = []

    def add_tour(self, tour):
        self.tours.append(tour)

    def show_tours(self):
        print("\n--- ДОСТУПНІ ТУРИ ---")

        for number, tour in enumerate(self.tours, 1):
            print(f"{number}. {tour.get_info()}")

    def find_by_direction(self, destination):
        for tour in self.tours:
            if tour.destination.lower() == destination.lower():
                yield tour

    def find_by_budget(self, budget):
        for tour in self.tours:
            if tour.calculate_price() <= budget:
                yield tour

    def __iter__(self):
        return iter(self.tours)


class BookingManager:
    def __init__(self):
        self.bookings = []

    def add_booking(self, booking):
        self.bookings.append(booking)

    def show_bookings(self):
        if not self.bookings:
            print("\nБронювань поки немає.")
            return

        print("\n--- БРОНЮВАННЯ ---")

        for number, booking in enumerate(self.bookings, 1):
            print(f"\nБронювання №{number}")
            print(booking.get_info())


class BookingContext:
    def __init__(self, booking):
        self.booking = booking

    def __enter__(self):
        print("\nОбробка бронювання...")
        return self.booking

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.booking.confirm()
            print("Бронювання підтверджено!")
        else:
            self.booking.cancel()

        return False


def create_tours(manager):
    manager.add_tour(
        BeachTour(
            "Відпочинок у Туреччині",
            "Анталія",
            25000,
            7
        )
    )

    manager.add_tour(
        ExcursionTour(
            "Екскурсія у Париж",
            "Париж",
            30000,
            5
        )
    )

    manager.add_tour(
        AdventureTour(
            "Пригода в Карпатах",
            "Карпати",
            18000,
            4
        )
    )

    manager.add_tour(
        BeachTour(
            "Відпочинок у Єгипті",
            "Хургада",
            22000,
            8
        )
    )


def book_tour(tour_manager, booking_manager):
    if not tour_manager.tours:
        print("Турів немає.")
        return

    tour_manager.show_tours()

    try:
        number = int(
            input("\nВиберіть номер туру: ")
        )

        if number < 1 or number > len(tour_manager.tours):
            raise ValueError(
                "Туру з таким номером не існує"
            )

        tour = tour_manager.tours[number - 1]

        print(f"\nВи вибрали: {tour.name}")

        name = input("Ім'я клієнта: ")
        phone = input("Телефон клієнта: ")

        if not name.strip():
            raise ValueError(
                "Ім'я клієнта не може бути порожнім"
            )

        tourists = int(
            input("Кількість туристів: ")
        )

        customer = Customer(name, phone)

        booking = Booking(
            customer,
            tour,
            tourists
        )

        with BookingContext(booking):
            pass

        booking_manager.add_booking(booking)

        print("\n--- РЕЗУЛЬТАТ ---")
        print(booking.get_info())

    except ValueError as error:
        print("\nПомилка:", error)


def search_tour(manager):
    print("\n--- ПОШУК ТУРУ ---")
    print("1 - За напрямком")
    print("2 - За бюджетом")

    choice = input("Ваш вибір: ")

    if choice == "1":
        destination = input("Введіть напрямок: ")

        found = False

        for tour in manager.find_by_direction(
            destination
        ):
            print(tour.get_info())
            found = True

        if not found:
            print("Турів не знайдено.")

    elif choice == "2":
        try:
            budget = float(
                input("Введіть максимальний бюджет: ")
            )

            found = False

            for tour in manager.find_by_budget(
                budget
            ):
                print(tour.get_info())
                found = True

            if not found:
                print("Турів не знайдено.")

        except ValueError:
            print("Введіть правильну суму.")

    else:
        print("Невірний вибір.")


def crash_test():
    print("\n--- КРАШ-ТЕСТ ---")

    try:
        price = float(input("Введіть ціну туру: "))

        if price <= 0:
            raise ValueError(
                "Ціна повинна бути більше 0"
            )

        duration = int(
            input("Введіть тривалість туру: ")
        )

        if duration <= 0:
            raise ValueError(
                "Тривалість повинна бути більше 0"
            )

        print("Дані правильні.")

    except ValueError as error:
        print("\nПОМИЛКА!")
        print(error)


def main():
    tour_manager = TourManager()
    booking_manager = BookingManager()

    create_tours(tour_manager)

    while True:
        print("\n==============================")
        print(" СИСТЕМА ТУРИСТИЧНОГО АГЕНТСТВА")
        print("==============================")
        print("1 - Показати тури")
        print("2 - Забронювати тур")
        print("3 - Пошук туру")
        print("4 - Показати бронювання")
        print("5 - Краш-тест")
        print("0 - Вихід")
        print("==============================")

        choice = input("Оберіть дію: ")

        if choice == "1":
            tour_manager.show_tours()

        elif choice == "2":
            book_tour(
                tour_manager,
                booking_manager
            )

        elif choice == "3":
            search_tour(tour_manager)

        elif choice == "4":
            booking_manager.show_bookings()

        elif choice == "5":
            crash_test()

        elif choice == "0":
            print("\nПрограму завершено.")
            break

        else:
            print("\nНевірний пункт меню.")


if __name__ == "__main__":
    main()