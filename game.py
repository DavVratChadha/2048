import numpy as np
import pygame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

COLOR_MAP = {
    0: "#FFFFFF",
    2: "#f5cf7d",
    4: "#f5c55d",
    8: "#f0bc4d",
    16: "#fcbc30",
    32: "#f5aa0a",
    64: "#fa8b14",
    128: "#ff8503",
    256: "#f78239",
    512: "#f78239",
    1024: "#fa7420",
    2048: "#fa6305",
    4096: "#fa5923",
    8192: "#fa4205",
    16384: "#fa2605",
    32768: "#f5372a",
    65536: "#f71302",
}

def new_board() -> np.array:
    return np.zeros((4,4))

def select_location(board: np.array) -> tuple[int, int]:
    zero_positions = (board == 0)
    true_indices = np.argwhere(zero_positions)
    if not np.any(true_indices):
        return None

    random_index = true_indices[np.random.choice(len(true_indices))]
    random_position = tuple(random_index)
    return random_position

def user_unput(penalty: int, old_moves: list[int]) -> int:
    move_played = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 1
                elif event.key == pygame.K_DOWN:
                    return 2
                elif event.key == pygame.K_LEFT:
                    return 3
                elif event.key == pygame.K_RIGHT:
                    return 4
        
def play_up(board: np.array = None) -> tuple[np.array, int]:
    new_board = np.copy(board)
    local_score = 0
    
    for col in range(4):
        #squeeze all values together
        free_row = 0
        for row in range(4):
            if new_board[row, col] != 0:
                new_board[free_row, col] = new_board[row, col]
                if row != free_row:
                    new_board[row, col] = 0
                free_row += 1
                
        #sum all values together
        free_row = 0
        for row in range(3):
            if new_board[row, col] != 0:
                if new_board[row, col] == new_board[row + 1, col]:
                    new_board[row, col] *= 2
                    local_score += new_board[row, col] #increase score
                    new_board[row + 1, col] = 0
                    
                new_board[free_row, col] = new_board[row, col]
                if row != free_row:
                    new_board[row, col] = 0
                free_row += 1
    return new_board, local_score

#everything is move up if you think it correctly
def play_down(board: np.array) -> tuple[np.array, int]:
    new_board = np.copy(board)
    new_board = np.rot90(new_board, k=2)
    new_board, local_score =  play_up(new_board)
    new_board = np.rot90(new_board, k=2)
    return new_board, local_score

def play_left(board: np.array) -> tuple[np.array, int]:
    new_board = np.copy(board)
    new_board = np.rot90(new_board, k=3)
    new_board, local_score =  play_up(new_board)
    new_board = np.rot90(new_board)
    return new_board, local_score

def play_right(board: np.array) -> tuple[np.array, int]:
    new_board = np.copy(board)
    new_board = np.rot90(new_board)
    new_board, local_score =  play_up(new_board)
    new_board = np.rot90(new_board, k=3)
    return new_board, local_score

def play(board: np.array, move: int) -> tuple[bool, np.array, int]:
    if move == 1:
        new_board, local_score = play_up(board)
    elif move == 2:
        new_board, local_score = play_down(board)
    elif move == 3:
        new_board, local_score = play_left(board)
    elif move == 4:
        new_board, local_score = play_right(board)
    
    valid = np.any(board != new_board)
    return valid, new_board, local_score
    
def player_move(board: np.array) -> tuple[np.array, int]:
    punish = 0
    old_moves = []
    while True:
        move = user_unput(punish, old_moves)
        valid, new_board, local_score = play(board, move)
        if valid:
            return new_board, local_score
        punish += 1

def color_grid(old_board: np.array):
    board = np.copy(old_board)
    board = np.rot90(board, k=3)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            value = board[i, j]
            color = COLOR_MAP.get(value, "#FFFFFF")  # Default to white if color not found
            patch = mpatches.Rectangle((i, j), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(patch)
            ax.text(i + 0.5, j + 0.5, str(int(value)), ha='center', va='center', color='black', fontsize=12)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, board.shape[1])
    ax.set_ylim(0, board.shape[0])
    ax.set_aspect('equal')
    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    #load the image from the BytesIO object + convert it to a Pygame surface
    plot_surface = pygame.image.load(buf, 'png').convert()
    
    plt.close(fig)
    return plot_surface

def game():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Pygame with Matplotlib Plot')
    clock = pygame.time.Clock()
    
    board = new_board()
    location = select_location(board)
    value = np.random.choice([2, 4], p = [0.9, 0.1])
    board[location] = value
    # location = select_location(board)
    # value = np.random.choice([2, 4], p = [0.9, 0.1])
    # board[location] = value
    score = 0
    print(f"Score = {score}")
    
    while True:
        location = select_location(board)
        if location is None:
            print("\n=========\nGame Over\n=========")
            return None
        
        value = np.random.choice([2, 4], p = [0.9, 0.1])
        board[location] = value
        
        #plot it all
        plot_surface  = color_grid(board)
        screen.fill((255, 255, 255))
        screen.blit(plot_surface, (50, 50))
        pygame.display.flip()
        clock.tick(30)
        
        board, local_score = player_move(board)
        score += local_score
        print(f"Score = {score}")
        

        

if __name__ == "__main__":
    try:
        game()
        input = input("Press enter to close game")
    except KeyboardInterrupt:
        print("Killing game")
    pygame.quit()