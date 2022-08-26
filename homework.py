class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # пройденная дистанция в километрах,
                                   # за время тренировки
                 speed: float,  # средняя скорость
                 calories: float  # количество израсходованных килокалорий
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения о выполненной тренировке."""
        # Для округления до тысячных долей используется форматирование f строк
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""

    # расстояние, которое спортсмен преодолевает за один шаг
    LEN_STEP: float = 0.65
    #  константа для перевода значений из метров в километры
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


# Наследуем класс Running от Training
class Running(Training):
    """Тренировка: бег."""

    # переопределяем родительский метод get_spent_calories()
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_in_min = self.duration * 60
        # помещаем метод get_mean_speed() в переменную для удобочитаемости
        avarage_speed = super().get_mean_speed()
        return ((coeff_calorie_1 * avarage_speed - coeff_calorie_2)
                * self.weight / self.M_IN_KM * duration_in_min)


# Наследуем класс SportsWalking от Training
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    # Пишем конструктор класса-наследника,
    # чтобы он принимал все нужные параметры
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height = height

    # переопределяем родительский метод get_spent_calories()
    def get_spent_calories(self) -> float:
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        duration_in_min = self.duration * 60
        # помещаем метод get_mean_speed() в переменную для удобочитаемости
        avarage_speed = super().get_mean_speed()
        return ((coeff_calorie_3 * self.weight
                + (avarage_speed**2 // self.height)
                * coeff_calorie_4 * self.weight) * duration_in_min)


# Наследуем класс Swimming от Training
class Swimming(Training):
    """Тренировка: плавание."""

    # переопределяем атрибут родительского класса:
    # расстояние, которое спортсмен преодолевает за один гребок.
    LEN_STEP: float = 1.38

    # Пишем конструктор класса-наследника,
    # чтобы он принимал все нужные параметры
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новые функциональности: свойство length_pool, count_pool
        self.length_pool = length_pool
        self.count_pool = count_pool

    # переопределяем родительский метод get_mean_speed()
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    # переопределяем родительский метод get_spent_calories()
    def get_spent_calories(self) -> float:
        coeff_calorie_5 = 1.1
        coeff_calorie_6 = 2
        return ((self.get_mean_speed() + coeff_calorie_5)
                * coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    work_dict = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}
    work_class = work_dict[workout_type]
    return work_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
