import pygame
import random
import time
import sys

# Constants
SORTING_SPEED = 0.02
ARRAY_SIZE = 100
WIDTH, HEIGHT = 1000, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (0, 255, 0)
GREEN = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame and the mixer
# You can adjust mixer settings as needed to avoid audio issues
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Made with ❤️ by Dark Phoenix")

# Load font for performance metrics
font = pygame.font.Font(None, 24)

# Load audio files using pygame.mixer
try:
    swap_sound = pygame.mixer.Sound(r"/home/darkphoenix/Downloads/squid.wav")
    done_sound = pygame.mixer.Sound(r"/home/darkphoenix/Downloads/done.wav")
except Exception as e:
    print(f"Error loading audio files: {e}")
    swap_sound = None
    done_sound = None

def generate_array():
    numbers = list(range(1, ARRAY_SIZE + 1))
    random.shuffle(numbers)
    return numbers

array = generate_array()

def draw_array(highlight_indices=[], swaps=0, comparisons=0, time_elapsed=0, sort_info=""):
    screen.fill(BLACK)
    bar_width = WIDTH // ARRAY_SIZE
    for i, val in enumerate(array):
        color = GREEN if i in highlight_indices else WHITE
        # drawing each bar; val*5 is used for a simple scaling effect
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - val * 5, bar_width, val * 5))
    
    metrics_text = f"{sort_info} | Swaps: {swaps} | Comparisons: {comparisons} | Time: {time_elapsed:.2f}s"
    text_surface = font.render(metrics_text, True, RED)
    screen.blit(text_surface, (10, 10))
    pygame.display.update()

def play_sound(sound_obj):
    if sound_obj:
        sound_obj.play()

def stop_sound(sound_obj):
    if sound_obj:
        sound_obj.stop()

def pulse_effect():
    # Play done sound at the start of the pulse effect
    if done_sound:
        play_sound(done_sound)
        
    start_time = time.time()
    # 7 second pulse effect transitioning through brightness levels
    while time.time() - start_time < 7:
        for brightness in range(100, 256, 5):
            screen.fill((brightness, brightness, brightness))
            pygame.display.update()
            time.sleep(0.015)
        for brightness in range(255, 99, -5):
            screen.fill((brightness, brightness, brightness))
            pygame.display.update()
            time.sleep(0.015)

def check_pause():
    pause_start = None
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_start = time.time()
                pygame.mixer.pause()
                # Wait for unpause
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:  # Unpause
                            pygame.mixer.unpause()
                            return time.time() - pause_start
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return 0

def bubble_sort():
    swaps, comparisons = 0, 0
    start_time = time.time()
    pause_duration = 0
    sort_info = "Bubble Sort | O(n²)"
    
    play_sound(swap_sound)
    
    for i in range(len(array) - 1):
        for j in range(len(array) - i - 1):
            pause_duration += check_pause()
            
            comparisons += 1
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swaps += 1
                draw_array([j, j + 1], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
                time.sleep(SORTING_SPEED)
    
    end_time = time.time()
    print()
    print("-------------------------------------")
    print("Bubble Sort")
    print("O(n^2) Complexity")
    print(f"Execution Time: {end_time - start_time - pause_duration:.4f} seconds")
    print("-------------------------------------")
    print()
    
    stop_sound(swap_sound)
    draw_array([], swaps, comparisons, end_time - start_time - pause_duration, sort_info)
    pulse_effect()

def merge_sort():
    swaps, comparisons = 0, 0
    start_time = time.time()
    pause_duration = 0
    sort_info = "Merge Sort | O(n log n)"

    if swap_sound:
        play_sound(swap_sound)

    def merge(low, mid, high):
        nonlocal swaps, comparisons, pause_duration
        left = array[low: mid + 1]
        right = array[mid + 1: high + 1]
        i = j = 0
        k = low
        while i < len(left) and j < len(right):
            pause_duration += check_pause()
            comparisons += 1
            if left[i] <= right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
                swaps += 1
            draw_array([k], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
            time.sleep(SORTING_SPEED)
            k += 1
        while i < len(left):
            pause_duration += check_pause()
            array[k] = left[i]
            i += 1
            swaps += 1
            draw_array([k], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
            time.sleep(SORTING_SPEED)
            k += 1
        while j < len(right):
            pause_duration += check_pause()
            array[k] = right[j]
            j += 1
            swaps += 1
            draw_array([k], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
            time.sleep(SORTING_SPEED)
            k += 1

    def merge_sort_recursive(low, high):
        if low < high:
            mid = (low + high) // 2
            merge_sort_recursive(low, mid)
            merge_sort_recursive(mid + 1, high)
            merge(low, mid, high)

    merge_sort_recursive(0, len(array) - 1)
    end_time = time.time()
    
    if swap_sound:
        stop_sound(swap_sound)
    
    draw_array([], swaps, comparisons, end_time - start_time - pause_duration, sort_info)
    print()
    print("-------------------------------------")
    print("Merge Sort")
    print("O(n log n) Complexity")
    print(f"Execution Time: {end_time - start_time - pause_duration:.4f} seconds")
    print("-------------------------------------")
    print()
    pulse_effect()

def quick_sort():
    swaps, comparisons = 0, 0
    start_time = time.time()
    pause_duration = 0
    sort_info = "Quick Sort | O(n log n)"

    if swap_sound:
        play_sound(swap_sound)

    def partition(low, high):
        nonlocal swaps, comparisons, pause_duration
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            pause_duration += check_pause()
            comparisons += 1
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                swaps += 1
                draw_array([i, j], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
                time.sleep(SORTING_SPEED)
        array[i + 1], array[high] = array[high], array[i + 1]
        swaps += 1
        draw_array([i + 1, high], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
        time.sleep(SORTING_SPEED)
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(array) - 1)
    end_time = time.time()
    
    if swap_sound:
        stop_sound(swap_sound)
    
    draw_array([], swaps, comparisons, end_time - start_time - pause_duration, sort_info)
    print()
    print("-------------------------------------")
    print("Quick Sort")
    print("O(n log n) Complexity")
    print(f"Execution Time: {end_time - start_time - pause_duration:.4f} seconds")
    print("-------------------------------------")
    print()
    pulse_effect()

def insertion_sort():
    swaps, comparisons = 0, 0
    start_time = time.time()
    pause_duration = 0
    sort_info = "Insertion Sort | O(n²)"
    
    if swap_sound:
        play_sound(swap_sound)
    
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            pause_duration += check_pause()
            comparisons += 1
            array[j + 1] = array[j]
            swaps += 1
            draw_array([j, j + 1], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
            time.sleep(SORTING_SPEED)
            j -= 1
        if j >= 0:
            comparisons += 1
        array[j + 1] = key
        draw_array([j + 1], swaps, comparisons, time.time() - start_time - pause_duration, sort_info)
        time.sleep(SORTING_SPEED)
    
    end_time = time.time()
    
    if swap_sound:
        stop_sound(swap_sound)
    
    draw_array([], swaps, comparisons, end_time - start_time - pause_duration, sort_info)
    print()
    print("-------------------------------------")
    print("Insertion Sort")
    print("O(n²) Complexity")
    print(f"Execution Time: {end_time - start_time - pause_duration:.4f} seconds")
    print("-------------------------------------")
    print()
    pulse_effect()

def inbuilt_sort():
    start_time = time.time()
    pause_duration = 0
    sort_info = "Python's Inbuilt Sort | O(n log n)"
    
    if swap_sound:
        play_sound(swap_sound)
    
    pause_duration += check_pause()
    array.sort()
    
    end_time = time.time()
    
    if swap_sound:
        stop_sound(swap_sound)
    
    draw_array([], 0, 0, end_time - start_time - pause_duration, sort_info)
    print()
    print("-------------------------------------")
    print("Python's Inbuilt Sort")
    print("O(n log n) Complexity")
    print(f"Execution Time: {end_time - start_time - pause_duration:.4f} seconds")
    print("-------------------------------------")
    print()
    pulse_effect()

def main():
    global array
    running = True
    paused = False
    draw_array()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    array = generate_array()
                    draw_array()
                elif event.key == pygame.K_s:
                    merge_sort()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()