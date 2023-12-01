import pygame
import sys
import numpy as np
import handwriting
from time import sleep

pygame.init()
FPS = 60
BORDER = 30
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600
WIDTH, HEIGHT = WINDOW_WIDTH - 2 * BORDER + 20, WINDOW_HEIGHT - 2 * BORDER + 20
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 40
BUTTON_DISTANCE = BUTTON_HEIGHT + 20
BUTTON_LOCATION_X = WINDOW_WIDTH - BORDER * 2 - BUTTON_WIDTH
BUTTON_LOCATION_Y = 3 * BORDER
PAINTING_SIZE = 1

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Handwriting recognition")
FONT = pygame.font.SysFont("Times New Roman", 25)
BIG_LINE = 6
SMALL_LINE = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY_LIGHT = (200, 200, 200)
BLUE_LIGHT = (180, 198, 231)
BLUE_DARK = (142, 170, 219)
BLUE_CLICK = (100, 140, 202)


def main():
    clock = pygame.time.Clock()
    clock.tick(FPS)
    drawing = True
    painting = np.zeros(shape=(28, 28))
    model = handwriting.NeuralNetwork()
    prediction = None

    while True:
        get_events()
        mouse = get_mouse_events()
        painting, drawing, prediction = draw_window(mouse, painting, drawing, prediction, model)


def get_mouse_events():
    return (
        pygame.mouse.get_pos()[0],
        pygame.mouse.get_pos()[1],
        pygame.mouse.get_pressed()
    )


def get_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def draw_window(mouse, painting, drawing, prediction, model):
    WINDOW.fill(GREY_LIGHT)

    # Painting
    painting = draw_canvas(mouse, painting, drawing)

    # Draw button
    painting, drawing = draw_button(
        mouse,
        BUTTON_LOCATION_X,
        BUTTON_LOCATION_Y,
        painting,
        drawing,
        "draw"
    )
    value = FONT.render("Draw", True, BLACK)
    WINDOW.blit(value, (BUTTON_LOCATION_X + 70, BUTTON_LOCATION_Y + 6))

    # Rubber button
    painting, drawing = draw_button(
        mouse,
        BUTTON_LOCATION_X,
        BUTTON_LOCATION_Y + BUTTON_DISTANCE,
        painting,
        drawing,
        "rubber"
    )
    value = FONT.render("Rubber", True, BLACK)
    WINDOW.blit(
        value, (BUTTON_LOCATION_X + 65, BUTTON_LOCATION_Y + BUTTON_DISTANCE + 6)
    )

    # Erase button
    painting, drawing = draw_button(
        mouse,
        BUTTON_LOCATION_X,
        BUTTON_LOCATION_Y + 2 * BUTTON_DISTANCE,
        painting,
        drawing,
        "erase"
    )
    value = FONT.render("Erase", True, BLACK)
    WINDOW.blit(
        value, (BUTTON_LOCATION_X + 70, BUTTON_LOCATION_Y + 2 * BUTTON_DISTANCE + 6)
    )

    # Predict button
    painting, drawing, prediction = draw_button(
        mouse,
        BUTTON_LOCATION_X,
        BUTTON_LOCATION_Y + 3 * BUTTON_DISTANCE,
        painting,
        drawing,
        "predict",
        prediction=prediction,
        model=model
    )
    value = FONT.render("Predict", True, BLACK)
    WINDOW.blit(
        value, (BUTTON_LOCATION_X + 70, BUTTON_LOCATION_Y + 3 * BUTTON_DISTANCE + 6)
    )

    # Output the prediction
    # Background
    pygame.draw.rect(
        WINDOW,
        BLACK,
        (
            BUTTON_LOCATION_X + 85,
            BUTTON_LOCATION_Y + 4 * BUTTON_DISTANCE - 3,
            33,
            40
        )
    )
    pygame.draw.rect(
        WINDOW,
        WHITE,
        (
            BUTTON_LOCATION_X + 88,
            BUTTON_LOCATION_Y + 4 * BUTTON_DISTANCE,
            27,
            34
        )
    )
    if prediction is not None:
        value = FONT.render(str(prediction), True, BLACK)
        WINDOW.blit(
            value, (BUTTON_LOCATION_X + 95, BUTTON_LOCATION_Y + 4 * BUTTON_DISTANCE + 6)
        )

    pygame.display.update()

    return painting, drawing, prediction


def draw_button(mouse, x, y, painting, drawing, type, prediction=None, model=None):
    mouse_x, mouse_y, click = mouse

    # Click on button
    if x < mouse_x < x + BUTTON_WIDTH and \
        y < mouse_y < y + BUTTON_HEIGHT and \
        click == (1, 0, 0):
        pygame.draw.rect(WINDOW, BLUE_CLICK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        if type == "draw":
            drawing = True
        elif type == "rubber":
            drawing = False
        elif type == "erase":
            drawing = True
            painting = np.zeros(shape=(28, 28))
        elif type == 'predict':
            prediction = model.get_number(painting)
            sleep(0.1)

    # Mouse on button
    elif x < mouse_x < x + BUTTON_WIDTH and \
        y < mouse_y < y + BUTTON_HEIGHT:
        pygame.draw.rect(WINDOW, BLUE_LIGHT, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))

    # Mouse off button
    else:
        if type == "draw" and drawing:
            pygame.draw.rect(WINDOW, BLUE_CLICK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        elif type == "draw" and not drawing:
            pygame.draw.rect(WINDOW, BLUE_DARK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        elif type == "rubber" and not drawing:
            pygame.draw.rect(WINDOW, BLUE_CLICK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        elif type == "rubber" and drawing:
            pygame.draw.rect(WINDOW, BLUE_DARK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        else:
            pygame.draw.rect(WINDOW, BLUE_DARK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(WINDOW, BLACK, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)

    if model is None:
        return painting, drawing
    else:
        return painting, drawing, prediction


def draw_canvas(mouse, painting, drawing):
    # Mouse coordinates
    mouse_x, mouse_y, click = mouse
    mouse_x, mouse_y = mouse_x - BORDER, mouse_y - BORDER

    # Black canvas border
    pygame.draw.rect(
        WINDOW,
        BLACK,
        (
            BORDER - 5,
            BORDER - 5,
            HEIGHT + 10,
            HEIGHT + 10
        )
    )

    # White canvas
    pygame.draw.rect(
        WINDOW,
        WHITE,
        (
            BORDER,
            BORDER,
            HEIGHT,
            HEIGHT
        )
    )

    # Drawing
    if click == (1, 0, 0) and drawing:
        for px_x in range(-PAINTING_SIZE, PAINTING_SIZE + 1):
            for px_y in range(-PAINTING_SIZE, PAINTING_SIZE + 1):
                if 0 <= mouse_x + px_x < len(painting[0]) * 20 and \
                    0 <= mouse_y + px_y < len(painting) * 20:
                    painting[int((mouse_y + px_y)/20)][int((mouse_x + px_x)/20)] = 1

    # Erasing
    elif click == (1, 0, 0) and not drawing:
        for px_x in range(-PAINTING_SIZE * 5, PAINTING_SIZE * 5 + 1):
            for px_y in range(-PAINTING_SIZE * 5, PAINTING_SIZE * 5 + 1):
                if 0 <= mouse_x + px_x < len(painting[0]) * 20 and \
                    0 <= mouse_y + px_y < len(painting) * 20:
                    painting[int((mouse_y + px_y)/20)][int((mouse_x + px_x)/20)] = 0

    # Show painting
    pixels_x, pixels_y = np.where(painting == 1)
    for x, y in zip(pixels_y, pixels_x):
        pygame.draw.rect(
            WINDOW,
            BLACK,
            (
                BORDER + x * 20,
                BORDER + y * 20,
                PAINTING_SIZE * 20,
                PAINTING_SIZE * 20,
            )
        )

    return painting


if __name__ == "__main__":
    main()