import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton

def calculate_card_value(card):
    if card in ('2', '3', '4', '5', '6'):
        return 1
    elif card in ('7', '8', '9'):
        return 0
    elif card in ('T', 'J', 'Q', 'K', 'A'):
        return -1
    else:
        return None

def calculate_true_count(card_count, num_decks, remaining_cards):
    return card_count / (num_decks * remaining_cards / 52)

class CardCountingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.card_count = 0
        self.num_decks = int(input("Enter the number of decks in the shoe: "))
        self.remaining_cards = self.num_decks * 52
        self.remaining_aces = self.num_decks * 4
        self.remaining_values = {str(i): self.num_decks * 4 for i in range(2, 10)}
        self.remaining_values.update({'T': self.num_decks * 4, 'J': self.num_decks * 4, 'Q': self.num_decks * 4,
                                      'K': self.num_decks * 4, 'A': self.num_decks * 4})

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("What's The Count?")
        self.setGeometry(100, 100, 400, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.card_count_label = QLabel(f"Hi-Lo Count: {self.card_count}")
        layout.addWidget(self.card_count_label)

        self.remaining_cards_label = QLabel(f"Total cards remaining: {self.remaining_cards}")
        layout.addWidget(self.remaining_cards_label)

        self.remaining_aces_label = QLabel(f"Aces remaining: {self.remaining_aces}")
        layout.addWidget(self.remaining_aces_label)

        self.remaining_values_labels = {}
        for value, count in self.remaining_values.items():
            value_label = QLabel(f"{value}: {count}")
            layout.addWidget(value_label)
            self.remaining_values_labels[value] = value_label

        true_count = calculate_true_count(self.card_count, self.num_decks, self.remaining_cards)
        self.true_count_label = QLabel(f"True Count: {true_count:.2f}")
        layout.addWidget(self.true_count_label)

        cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        for card in cards:
            btn = QPushButton(card)
            btn.clicked.connect(lambda _, c=card: self.on_card_click(c))
            layout.addWidget(btn)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_shoe)
        layout.addWidget(reset_btn)

    def update_card_count(self, card):
        card_value = calculate_card_value(card)
        if card_value is not None:
            self.card_count += card_value
            self.card_count_label.setText(f"Hi-Lo Count: {self.card_count}")
            self.remaining_cards -= 1
            self.remaining_cards_label.setText(f"Total cards remaining: {self.remaining_cards}")

            if card == 'A':
                self.remaining_aces -= 1
                self.remaining_aces_label.setText(f"Aces remaining: {self.remaining_aces}")

            self.remaining_values[card] -= 1
            self.remaining_values_labels[card].setText(f"{card}: {self.remaining_values[card]}")

            true_count = calculate_true_count(self.card_count, self.num_decks, self.remaining_cards)
            self.true_count_label.setText(f"True Count: {true_count:.2f}")

    def on_card_click(self, card):
        self.update_card_count(card)

    def reset_shoe(self):
        self.card_count = 0
        self.remaining_cards = self.num_decks * 52
        self.remaining_aces = self.num_decks * 4
        self.remaining_values = {str(i): self.num_decks * 4 for i in range(2, 10)}
        self.remaining_values.update({'T': self.num_decks * 4, 'J': self.num_decks * 4, 'Q': self.num_decks * 4,
                                      'K': self.num_decks * 4, 'A': self.num_decks * 4})

        self.card_count_label.setText(f"Hi-Lo Count: {self.card_count}")
        self.remaining_cards_label.setText(f"Total cards remaining: {self.remaining_cards}")
        self.remaining_aces_label.setText(f"Aces remaining: {self.remaining_aces}")

        for value, count in self.remaining_values.items():
            self.remaining_values_labels[value].setText(f"{value}: {count}")

        self.true_count_label.setText("True Count: 0.00")

    def keyPressEvent(self, event):
        key = event.text().upper()
        if key in ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'):
            self.on_card_click(key)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardCountingApp()
    window.show()
    sys.exit(app.exec_())
