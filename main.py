import tkinter as tk
from PIL import Image, ImageTk
import os

# Constantes
TILE_SIZE = 94
GRID_W, GRID_H = 4, 4


game_matrix = [
    [0, 0, 1, 1],  # Fila 0
    [0, 1, 1, 1],  # Fila 1 (pared en [1][1])
    [0, 1, "E", 1],  # Fila 2 (enemigo en [2][2])
    ["P", 0, 1, 0]   # Fila 3 (jugador en [3][0])
]


def cargar_imagen(ruta, size=(TILE_SIZE, TILE_SIZE)):
    img = Image.open(ruta).resize(size)
    return ImageTk.PhotoImage(img)

def crear_escenario_desde_matriz(canvas, floor_img, wall_img, enemy_img):
    canvas.delete("all")  # Limpiar el lienzo
    for y, fila in enumerate(game_matrix):
        for x, celda in enumerate(fila):
            if celda == 0:  # Suelo
                canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=floor_img, anchor='nw')
            elif celda == 1:  # Pared
                canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=wall_img, anchor='nw')
            elif celda == "E":  # Enemigo
                canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=enemy_img, anchor='nw')


# Función para que el enemigo destruya paredes con animación
def enemigo_destruir_pared(canvas, floor_img, wall_img, enemy_frames):
    # Buscar la posición del enemigo en la matriz
    for y, fila in enumerate(game_matrix):
        for x, celda in enumerate(fila):
            if celda == "E":
                # Buscar paredes adyacentes al enemigo
                if y > 0 and game_matrix[y - 1][x] == 1:  # Arriba
                    game_matrix[y - 1][x] = 0
                elif y < len(game_matrix) - 1 and game_matrix[y + 1][x] == 1:  # Abajo
                    game_matrix[y + 1][x] = 0
                elif x > 0 and game_matrix[y][x - 1] == 1:  # Izquierda
                    game_matrix[y][x - 1] = 0
                elif x < len(fila) - 1 and game_matrix[y][x + 1] == 1:  # Derecha
                    game_matrix[y][x + 1] = 0

                # Animar al enemigo
                animar_enemigo(canvas, x, y, enemy_frames)
                
                # Actualizar el lienzo después de destruir la pared
                crear_escenario_desde_matriz(canvas, floor_img, wall_img, enemy_frames[0])
                return  # Salir después de destruir una pared

def poner_pared(canvas, wall_img, posx, posy):
    canvas.create_image(posx * TILE_SIZE, posy * TILE_SIZE, image=wall_img, anchor='nw')


def cargar_frames_enemigo():
    enemy_frames = []
    for i in range(5):
        try:
            ruta = os.path.join("charact", f"adventurer-run-0{i}.png")
            print(f"Cargando {ruta}...")
            img = Image.open(ruta).resize((TILE_SIZE, TILE_SIZE))
            enemy_frames.append(ImageTk.PhotoImage(img))
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen {ruta}")
            return None
    return enemy_frames

def animar_enemigo(canvas, frames, frame_idx, x, y, enemigo_id=None):
    if enemigo_id is not None:
        canvas.delete(enemigo_id)
    enemigo_id = canvas.create_image(x, y, image=frames[frame_idx], anchor='nw')
    # Cambia de frame recursivamente
    def siguiente_frame():
        animar_enemigo(canvas, frames, (frame_idx + 1) % len(frames), x, y, enemigo_id)
    canvas.after(120, siguiente_frame)

def mover_enemigo(canvas, frames, grid, pos, wall_pos, frame_idx=0, enemigo_id=None):
    x, y = pos
    # Si el enemigo choca con la pared, no avanza
    if (x+1, y) == wall_pos:
        next_pos = (x, y)
    else:
        next_pos = (x+1 if x+1 < GRID_W else 0, y if x+1 < GRID_W else (y+1 if y+1 < GRID_H else 0))
    if enemigo_id is not None:
        canvas.delete(enemigo_id)
    enemigo_id = canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=frames[frame_idx], anchor='nw')
    def siguiente():
        mover_enemigo(canvas, frames, grid, next_pos, wall_pos, (frame_idx+1)%len(frames), enemigo_id)
    canvas.after(250, siguiente)

def animar_enemigo(canvas, x, y, enemy_frames, frame_index=0):
    if frame_index < len(enemy_frames):
        canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=enemy_frames[frame_index], anchor='nw')
        canvas.after(100, animar_enemigo, canvas, x, y, enemy_frames, frame_index + 1)

def main():
    root = tk.Tk()
    root.title("Taller Tkinter - Recursividad y Enemigos")
    canvas = tk.Canvas(root, width=GRID_W*TILE_SIZE, height=GRID_H*TILE_SIZE) #
    canvas.pack()

    # Cargar imágenes
    floor_img = cargar_imagen(os.path.join("floor", "floor_tiles.png"))
    wall_img = ImageTk.PhotoImage(Image.open("wall_1.png").resize((TILE_SIZE, TILE_SIZE)))
    # wall_img = cargar_imagen("wall_1.png")

    enemy_frames = cargar_frames_enemigo()
    # enemy_frames_verde = cargar_frames_enemigo()
    # Crear escenario (suelo)
    crear_escenario_desde_matriz(canvas, floor_img, wall_img, enemy_frames[0])

    # Colocar una pared en (2,1)
    wall_pos = (2, 1)
    # poner_pared(canvas, wall_img, *wall_pos)

    
    # Animar enemigo que se mueve y se detiene ante la pared
    btn_destruir = tk.Button(root, text="Enemigo destruye", command=lambda: enemigo_destruir_pared(canvas, floor_img, wall_img, enemy_frames))
    btn_destruir.pack()


    root.mainloop()

if __name__ == "__main__":
    main()