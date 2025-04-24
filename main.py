import tkinter as tk
from PIL import Image, ImageTk
import os

# Constantes
TILE_SIZE = 94
GRID_W, GRID_H = 4, 4

def cargar_imagen(ruta, size=(TILE_SIZE, TILE_SIZE)):
    img = Image.open(ruta).resize(size)
    return ImageTk.PhotoImage(img)

def crear_escenario(canvas, floor_img, x=0, y=0):
    if y >= GRID_H:
        return
    if x < GRID_W:
        canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=floor_img, anchor='nw')
        crear_escenario(canvas, floor_img, x + 1, y)
    else:
        crear_escenario(canvas, floor_img, 0, y + 1)

def poner_pared(canvas, wall_img, posx, posy):
    canvas.create_image(posx * TILE_SIZE, posy * TILE_SIZE, image=wall_img, anchor='nw')

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
    
def main():
    root = tk.Tk()
    root.title("Taller Tkinter - Recursividad y Enemigos")
    canvas = tk.Canvas(root, width=GRID_W*TILE_SIZE, height=GRID_H*TILE_SIZE)
    canvas.pack()

    # Cargar imágenes
    floor_img = cargar_imagen(os.path.join("floor", "floor_tiles.png"))
    wall_img = cargar_imagen("wall_1.png")
    enemy_frames = []
    for i in range(5):
        ruta = os.path.join("charact", f"adventurer-run-0{i}.png")
        enemy_frames.append(cargar_imagen(ruta))

    # Crear escenario (suelo)
    crear_escenario(canvas, floor_img)

    # Colocar una pared en (2,1)
    wall_pos = (2, 1)
    poner_pared(canvas, wall_img, *wall_pos)

    # Animar enemigo que se mueve y se detiene ante la pared
    mover_enemigo(canvas, enemy_frames, (GRID_W, GRID_H), (0, 1), wall_pos)

    root.mainloop()

if __name__ == "__main__":
    main()