from typing import Dict, Type, Union
from dataclasses import dataclass
@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration_hour: float
    distance_km: float
    speed_km_hour: float
    calories: float

    def get_message(self) -> str:
        """Возвращает данные о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration_hour:.3f} ч.; '
                f'Дистанция: {self.distance_km:.3f} км; '
                f'Ср. скорость: {self.speed_km_hour:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOURS_TO_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration_hour: float,
                 weight: float,
                 ) -> None:
        """Создает конструктор класса с аргументами."""
        self.action: int = action
        self.duration_hour: float = duration_hour
        self.weight: float = weight

    def get_distance_km(self) -> float:
        """Получить дистанцию в км."""
        distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed_km_hour(self) -> float:
        """Получить среднюю скорость движения."""
        speed_km_hour: float = self.get_distance_km() / self.duration_hour
        return speed_km_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите калории') 

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration_hour,
                                   self.get_distance_km(),
                                   self.get_mean_speed_km_hour(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_speed_km_hour_MULTIPLIER: int = 18
    CALORIES_MEAN_speed_km_hour_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных за тренировку калорий."""
        cal: float = self.CALORIES_MEAN_speed_km_hour_MULTIPLIER * self.get_mean_speed_km_hour() - self.CALORIES_MEAN_speed_km_hour_SHIFT
        calories: float = cal * self.weight / self.M_IN_KM * self.duration_hour * self.HOURS_TO_MIN
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_MULTIPLICATION_WEIGHT: float = 0.035
    CALORIES_MEAN_MULTIPLICATION_speed_km_hour: int = 2
    CALORIES_MEAN_MULTIPLICATION_SOMETHING_ELSE: float = 0.029

    def __init__(self,
                 action: int,
                 duration_hour: float,
                 weight: float,
                 height: int) -> None:
        """Создает конструктор класса с аргументами."""
        super().__init__(action, duration_hour, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных за тренировку калорий."""
        calories_1: float = self.CALORIES_MEAN_MULTIPLICATION_WEIGHT * self.weight
        calories_2: float = self.get_mean_speed_km_hour() ** self.CALORIES_MEAN_MULTIPLICATION_speed_km_hour // self.height
        calories_3: float = calories_2 * self.CALORIES_MEAN_MULTIPLICATION_SOMETHING_ELSE * self.weight
        calories: float = (calories_1 + calories_3) * self.duration_hour * self.HOURS_TO_MIN
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_PLUS_speed_km_hour: float = 1.1
    CALORIES_MEAN_SOME_MULTIPLICATION: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration_hour: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        """Создает конструктор класса с аргументами."""
        super().__init__(action, duration_hour, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed_km_hour(self) -> float:
        """Получить среднюю скорость движения."""
        speed_km_hour_1: int = self.length_pool * self.count_pool
        self.speed_km_hour: float = speed_km_hour_1 / super().M_IN_KM / self.duration_hour
        return self.speed_km_hour

    def get_spent_calories(self) -> float:
        """Возвращает количество потраченных за тренировку калорий."""
        calories_1: float = self.get_mean_speed_km_hour() + self.CALORIES_MEAN_PLUS_speed_km_hour
        calories: float = calories_1 * self.CALORIES_MEAN_SOME_MULTIPLICATION * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: Dict[str,Type[Union[Swimming, Running, SportsWalking]]] = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in type_dict:
        raise NotImplementedError('Неизвестный тип тренировки') 
    return type_dict[workout_type](*data)


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
