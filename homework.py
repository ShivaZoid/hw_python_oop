from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.

    Args:
        training_type (str): имя класса тренировки.
        duration (float): длительность тренировки в часах.
        distance (float): пройденная дистанция в километрах, за время.
                          тренировки.
        speed (float): средняя скорость.
        calories (float): количество израсходованных килокалорий.
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = ("Тип тренировки: {training_type}; "
               "Длительность: {duration:.3f} ч.; "
               "Дистанция: {distance:.3f} км; "
               "Ср. скорость: {speed:.3f} км/ч; "
               "Потрачено ккал: {calories:.3f}.")

    def get_message(self):
        """Возвращает строку сообщения о выполненной тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки.

    Attributes:
        LEN_STEP (float): Расстояние, которое спортсмен преодолевает за один
                          шаг.
        M_IN_KM (float): константа для перевода значений из метров в километры.
        HR_IN_MIN(float): константа для перевода значений из часов в минуты.
        coeff_calorie_1 (float): константа, неименованное значение.
        coeff_calorie_2 (float): константа, неименованное значение.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HR_IN_MIN: float = 60
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """ Args:
            action (int): количество совершённых действий.
            duration (float): длительность тренировки.
            weight (float): вес спортсмена.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def duration_in_min(self) -> float:
        """Длительность тренировки в минутах"""
        return self.duration * self.HR_IN_MIN

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(self.__class__.__name__
                                  + 'Redefine get_spent_calories()')

    def training_name(self) -> str:
        """Получить имя класса тренировки"""
        return (self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.training_name(),
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег.

    Наследуем класс Running от Training
    """

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Переопределяем родительский метод для Running.
        """
        # помещаем метод get_mean_speed() в переменную для удобочитаемости
        avarage_speed = self.get_mean_speed()
        return ((self.coeff_calorie_1 * avarage_speed - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration_in_min())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Наследуем класс SportsWalking от Training.

    Attributes:
        coeff_calorie_3 (float): константа, неименованное значение.
        coeff_calorie_4 (float): константа, неименованное значение.
    """

    coeff_calorie_3: float = 0.035  # константа
    coeff_calorie_4: float = 0.029

    # Пишем конструктор класса-наследника,
    # чтобы он принимал все нужные параметры
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """ Args:
            action (int): количество совершённых действий.
            duration (float): длительность тренировки.
            weight (float): вес спортсмена.
            height (float): рост спортсмена.
        """
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Переопределяем родительский метод для SportsWalking.
        """
        # помещаем метод get_mean_speed() в переменную для удобочитаемости
        avarage_speed = self.get_mean_speed()
        return ((self.coeff_calorie_3 * self.weight
                + (avarage_speed**2 // self.height)
                * self.coeff_calorie_4 * self.weight) * self.duration_in_min())


class Swimming(Training):
    """Тренировка: плавание.

    Наследуем класс Swimming от Training.

    Attributes:
        LEN_STEP (float): переопределяем атрибут родительского класса:
        расстояние, которое спортсмен преодолевает за один гребок.
        coeff_calorie_5 (float): константа, неименованное значение.
        coeff_calorie_6 (float): константа, неименованное значение.
    """

    LEN_STEP: float = 1.38
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: float = 2

    # Пишем конструктор класса-наследника,
    # чтобы он принимал все нужные параметры
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        """ Args:
            action (int): количество совершённых действий.
            duration (float): длительность тренировки.
            weight (float): вес спортсмена.
            length_pool (float): длина бассейна в метрах.
            count_pool (float): сколько раз пользователь переплыл бассейн.
        """
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новые функциональности: свойство length_pool, count_pool
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.

        переопределяем родительский метод для Swimming.
        """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Переопределяем родительский метод для Swimming.
        """
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    work_dict: Dict[str, float] = {'SWM': Swimming,
                                   'RUN': Running,
                                   'WLK': SportsWalking}
    try:
        work_class = work_dict[workout_type]
    except KeyError:
        print(f"There is no such training '{workout_type}'")
    else:
        return work_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
