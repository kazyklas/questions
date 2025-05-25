import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt

def load_question_sets(filename):
    """
    Loads question sets from a text file.
    Each set starts with a line beginning with '#', followed by questions.
    Returns a tuple: (list of question lists, list of set names)
    """
    question_sets = []
    current_set = []
    set_names = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                # Start of a new set
                if current_set:
                    question_sets.append(current_set)
                    current_set = []
                set_names.append(line.lstrip('#').strip())
            else:
                current_set.append(line)
        if current_set:
            question_sets.append(current_set)
    # If no set names, use default names
    if not set_names or len(set_names) != len(question_sets):
        set_names = [f"Question Set {i+1}" for i in range(len(question_sets))]
    return question_sets, set_names

class QuestionPage(QWidget):
    """
    Widget for displaying a single set of questions, one at a time,
    with navigation buttons and a back button.
    """
    def __init__(self, questions, on_back, parent=None):
        super().__init__(parent)
        self.questions = questions
        self.current_index = 0  # Track which question is currently shown
        self.on_back = on_back  # Callback to go back to selection page

        # Main layout for the page
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)

        # Label to display the current question
        self.question_label = QLabel(self.questions[self.current_index])
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setObjectName("QuestionLabel")
        self.layout.addWidget(self.question_label)

        # Navigation buttons (Previous/Next)
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.setObjectName("SetButton")
        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("SetButton")
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)

        # Back to Selection button
        self.back_button = QPushButton("Back to Selection")
        self.back_button.setObjectName("SetButton")
        self.layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.on_back)

        self.setLayout(self.layout)
        self.update_buttons()

    def show_previous(self):
        """Show the previous question if possible."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_question()

    def show_next(self):
        """Show the next question if possible."""
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.update_question()

    def update_question(self):
        """Update the label to show the current question."""
        self.question_label.setText(self.questions[self.current_index])
        self.update_buttons()

    def update_buttons(self):
        """Enable/disable navigation buttons based on position."""
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.questions) - 1)

class SelectionPage(QWidget):
    """
    Widget for the first page, allowing the user to select a question set.
    """
    def __init__(self, on_select, names, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        # Title label
        label = QLabel("Choose a Question Set")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("TitleLabel")
        layout.addWidget(label)
        # Create a button for each question set
        for i, name in enumerate(names):
            btn = QPushButton(name)
            btn.setMinimumHeight(40)
            btn.setObjectName("SetButton")
            btn.clicked.connect(lambda checked, idx=i: on_select(idx))
            layout.addWidget(btn)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    """
    Main application window. Handles switching between selection and question pages.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question App")
        self.resize(500, 350)
        self.stacked = QStackedWidget()  # Stack for switching between pages
        self.setCentralWidget(self.stacked)

        # Load questions and set names from file
        self.question_sets, self.set_names = load_question_sets('questions.txt')

        # Create and add the selection page
        self.selection_page = SelectionPage(self.show_questions, self.set_names)
        self.stacked.addWidget(self.selection_page)

        self.question_page = None  # Will hold the current QuestionPage

        # Apply Green Light Theme styling
        # Load stylesheet from external file (style.qss)
        try:
            with open("style.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Could not load stylesheet:", e)

    def show_questions(self, set_index):
        """
        Switch to the QuestionPage for the selected set.
        """
        if self.question_page:
            self.stacked.removeWidget(self.question_page)
            self.question_page.deleteLater()
        self.question_page = QuestionPage(self.question_sets[set_index], self.show_selection)
        self.stacked.addWidget(self.question_page)
        self.stacked.setCurrentWidget(self.question_page)

    def show_selection(self):
        """
        Switch back to the selection page.
        """
        self.stacked.setCurrentWidget(self.selection_page)

if __name__ == "__main__":
    # Entry point for the application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
