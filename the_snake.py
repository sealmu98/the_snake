from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка by sealmu98')

# Настройка времени:
clock = pygame.time.Clock()


# Описание всех классов:
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self,
                 position: tuple[int, int] = None,
                 body_color: tuple[int, int, int] = None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """
    Унаследованный класс от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self, position: tuple[int, int] = None):
        super().__init__(position, APPLE_COLOR)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Установить случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        return self.position

    def draw(self, surface):
        """Отрисовать яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Унаследованный класс от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self,
                 position: tuple[int, int] = ((SCREEN_WIDTH // 2),
                                              (SCREEN_HEIGHT // 2))
                 ):
        super().__init__(position, SNAKE_COLOR)
        self.length = 2
        self.positions = [position]
        self.direction = UP
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновить направление после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновить позицию змейки."""
        # Получение текущей головной позиции:
        head_position = self.get_head_position()

        # Вычисление новой позиции головы:
        new_head_position = ((head_position[0] + self.direction[0] * GRID_SIZE)
                             % SCREEN_WIDTH,
                             (head_position[1] + self.direction[1] * GRID_SIZE)
                             % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)

        # Обновление списка позиций:
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывать змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Вернуть позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние после столкновения с собой."""
        self.__init__()


def handle_keys(game_object: Snake):
    """Обработать нажатия клавиш, чтобы изменить направление движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция запуска."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Управление змейкой:
        handle_keys(snake)

        # Обновление направления и положения змейки:
        snake.update_direction()
        snake.move()

        # Реалтзация роста змейки:
        if snake.get_head_position() == apple.position:
            # Проверка позиции яблока внутри змейки:
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
            snake.length += 1

        # Проверка на столкновение с собой:
        # Когда голова змеии поподает на координату тела,
        # в кортеже positions получается две одинаковых координаты
        # так как множество не может содерджать дубликаты элементов
        # там на одну координату меньше
        if len(snake.positions) > len(set(snake.positions)):
            snake.reset()

        # Реализация отрисовки на экране:
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
