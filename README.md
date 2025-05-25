# Question App

A simple PyQt5 application for displaying and navigating through sets of questions. You can easily add or edit questions by modifying a text file.

---

## Requirements

- Python 3.7+
- PyQt5

Install dependencies with:

```
pip install -r requirements.txt
```

---

## Running the Application

1. Make sure you have Python installed.
2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Run the application:

   ```
   python main.py
   ```

---

## Editing and Adding Questions

Questions are stored in `questions.txt` in the following format:

```
# Set 1
Question 1 for set 1
Question 2 for set 1

# Set 2
Question 1 for set 2
Question 2 for set 2

# Set 3
Question 1 for set 3
Question 2 for set 3
```

- Each set starts with a line beginning with `#` followed by the set name.
- Each subsequent line is a question belonging to that set.
- Leave a blank line between sets for readability (optional).

**To add more questions:**
- Add new questions under the appropriate set header.
- To add a new set, start a new section with `# Set Name` and add questions below it.

**Example:**

```
# Icebreakers
What's your favorite color?
What's your dream vacation?

# Deep Thoughts
What motivates you in life?
If you could change one thing about the world, what would it be?
```

---

## Customization

- All colors and styles are defined in the code using the Green Light Theme palette.
- To change the look, edit the stylesheet section in `main.py`.

---

## Support

If you encounter issues or have suggestions, please open an issue or contact the maintainer.
