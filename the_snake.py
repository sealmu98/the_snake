from random import choice, randint

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

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание всех классов
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, который предназначен для переопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Унаследованный класс от GameObject, описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод который устанавливает случайное положение яблока на игровом поле."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод который отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Унаследованный класс от GameObject, описывающий змейку и её поведение."""

    def __init__(self,
                 positions=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 length=1,
                 body_color=SNAKE_COLOR):

        super().__init__(body_color)
        self.lenght = length
        self.positions = [positions]
        self.direction = UP
        self.next_direction = None
        self.body_color = body_color
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновления позиции змейки."""
        # Получение текущей головной позиции
        head_position = self.get_head_position()

        # Вычисление новой позиции головы
        new_head_position = (
            head_position[0] + self.direction[0] * GRID_SIZE,
            head_position[1] + self.direction[1] * GRID_SIZE)

        if (not (0 <= new_head_position[0] < SCREEN_WIDTH
                 and 0 <= new_head_position[1] < SCREEN_HEIGHT) or
                new_head_position in self.positions[2:]):
            return self.reset

        # Проверка на столкновение с собой
        if new_head_position in self.position[2:]:
            return self.reset

        # Обновление списка позиций
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод который отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


    def get_head_position(self):
        """Метод который возвращает позицию головы змейки."""
        return self.position[0]

    def reset(self):
        """
        Метод который сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        pass

    def handle_keys(self):
        """
        Метод котрый обрабатывает нажатия клавиш,
        чтобы изменить направление движения змейки.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT


def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple()

    snake = Snake()

    while True:
        clock.tick(SPEED)

        snake.handle_keys()

        snake.update_direction()
        snake.move

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None


# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT
