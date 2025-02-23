import tkinter as tk
from tkinter import messagebox
from functools import partial

class Game_logic:
    def __init__(self):
        self.current_p = "X"

    def switch_p(self):
        self.current_p = "O" if self.current_p == "X" else "X"

    def check_winner(self, buttons):
        # winner check
        winning_patterns = [
            # Rows
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],

            # Columns
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],

            # Diagonals
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]

        for pattern in winning_patterns:
            value = [buttons[pos].cget("text") for pos in pattern]
            if value[0] !="" and value[0]==value[1]==value[2]:
                return value[0]
            
        if all(buttons[pos].cget("text")!="" for pos in buttons):
            return "Draw"
        return None

    def reset(self, buttons): 
        # Reset the game to its initial state
        for pos in buttons:
            buttons[pos].config(text="")
        self.current_p = "X"  # Reset to player X


class Gui:
    def __init__(self, root, game_logic):
        self.root = root
        self.game_logic = game_logic
        self.buttons = {}
        self.create_ui()

    def create_ui(self):
        self.root.geometry("300x500")
        self.root.resizable(False,False)
        self.btk_render()

    def btk_render(self):
        # button render
        for row in range(3):
            self.root.grid_rowconfigure(row,weight=1)
            for col in range(3):
                self.root.grid_columnconfigure(col,weight=1)
                btk = tk.Button(self.root, text="", command=partial(self.on_click, row, col))
                btk.grid(row=row, column=col,sticky="nsew")
                self.buttons[(row, col)] = btk
    
    def on_click(self, row, col):
        if self.buttons[(row, col)]["text"] == "":
            self.buttons[(row, col)].config(text=self.game_logic.current_p)

            # Check if there's a winner
            winner = self.game_logic.check_winner(self.buttons)
            if winner:
                if winner == "Draw":
                    messagebox.showinfo("Game Over", "It's a Draw!")
                else:
                    messagebox.showinfo("Game Over", f"Player {winner} Wins!")
                
                self.reset_board()  # Reset the board after a win or draw
            else:
                self.game_logic.switch_p()
        else:
            messagebox.showinfo("Note", "THIS BOX IS OCCUPIED!!")

    def reset_board(self):
        # Reset the board after a win or draw
        self.game_logic.reset(self.buttons)

# Object creation
# Initialize root tk.Tk()
root = tk.Tk()
# Window creation
root.title("TIC-TAC-TOE")
root.geometry("300x300")
# Object making
game_logic = Game_logic()
game = Gui(root, game_logic)
# Tkinter mainloop run
root.mainloop()
