from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

Window.clearcolor = (0.1, 0.1, 0.1, 1)
Window.title = "X"

class TicTacToeGrid(GridLayout):
    def __init__(self, **kwargs):
        super(TicTacToeGrid, self).__init__(**kwargs)
        self.cols = 3
        self.reset_game()

    def reset_game(self):
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_player = 'X'
        self.clear_widgets()

        for row in range(3):
            for col in range(3):
                button = Button(
                    text='',
                    font_size=48,
                    background_color=(0.2, 0.2, 0.2, 1),
                    color=(1, 1, 1, 1),
                    size_hint=(1, 1),
                    font_name='Roboto'
                )
                button.bind(on_press=self.make_move)
                button.coords = (row, col)
                self.add_widget(button)

    def make_move(self, instance):
        row, col = instance.coords

        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            instance.text = self.current_player
            instance.background_color = (1, 0.5, 0.5, 1) if self.current_player == 'X' else (0.5, 0.5, 1, 1)

            anim = Animation(font_size=64, duration=0.2) + Animation(font_size=48, duration=0.2)
            anim.start(instance)

            if self.check_winner():
                self.show_popup(f"Player {self.current_player} wins!")
            elif self.check_draw():
                self.show_popup("It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if all([self.board[i][j] == self.current_player for j in range(3)]) or \
               all([self.board[j][i] == self.current_player for j in range(3)]):
                return True
        if all([self.board[i][i] == self.current_player for i in range(3)]) or \
           all([self.board[i][2-i] == self.current_player for i in range(3)]):
            return True
        return False

    def check_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def show_popup(self, message):
        layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message, font_size=32)
        close_button = Button(text='Restart Game', size_hint=(1, 0.3))
        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title='Game Over', content=layout, size_hint=(0.5, 0.5))

     
        def on_close(instance):
            self.reset_game()  
            popup.dismiss()  

        close_button.bind(on_press=on_close)
        popup.open()

class TicTacToeApp(App):
    def build(self):
        return TicTacToeGrid()

if __name__ == '__main__':
    TicTacToeApp().run()