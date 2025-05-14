import streamlit as st
import random

# -------------------- Motivational Quotes -------------------- #
QUOTES = [
    "Keep going, you're doing great!",
    "Small steps every day lead to big changes.",
    "Discipline is stronger than motivation.",
    "Progress over perfection.",
    "Habits define who we become.",
    "You don’t have to be extreme, just consistent.",
    "Success is the product of daily habits—not once-in-a-lifetime transformations."
]

def get_random_quote():
    return random.choice(QUOTES)

# -------------------- OOP Classes -------------------- #
class Habit:
    def __init__(self, name):
        self.name = name
        self.history = []  # List of True/False values

    def add_entry(self, done: bool):
        self.history.append(done)

    def consistency_rate(self):
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)

    def last_7_days(self):
        return self.history[-7:]  # Show last 7 entries

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit: Habit):
        self.habits.append(habit)

    def get_burnout_risk(self):
        if len(self.habits) > 5:
            return "⚠️ You're tracking a lot of habits — be careful of burnout!"
        for habit in self.habits:
            if len(habit.history) >= 5 and habit.consistency_rate() < 0.4:
                return f"😓 You're struggling with **{habit.name}** — consider simplifying it."
        return "✅ You're doing great! Keep the balance."

    def get_suggestions(self):
        tips = []
        for habit in self.habits:
            rate = habit.consistency_rate()
            if len(habit.history) >= 3 and rate < 0.5:
                tips.append(f"🔄 Try simplifying or replacing **{habit.name}** with something more achievable.")
        return tips

# -------------------- Streamlit UI -------------------- #
st.set_page_config(page_title="HabitForge - Smart Habit Tracker", layout="centered")
st.title("Smart Habit Routine")


if "tracker" not in st.session_state:
    st.session_state.tracker = HabitTracker()
if "habit_names" not in st.session_state:
    st.session_state.habit_names = []

# Sidebar - Add New Habit
st.sidebar.header("➕ Add a New Habit")
habit_name = st.sidebar.text_input("Habit Name")

if st.sidebar.button("Add Habit"):
    if habit_name and habit_name not in st.session_state.habit_names:
        habit = Habit(habit_name)
        st.session_state.tracker.add_habit(habit)
        st.session_state.habit_names.append(habit_name)
        st.sidebar.success(f"Added habit: {habit_name}")
    elif habit_name in st.session_state.habit_names:
        st.sidebar.warning("Habit already exists.")
    else:
        st.sidebar.warning("Please enter a valid habit name.")

# Main - Track Habits
st.subheader("📅 Mark Today's Habits")
if not st.session_state.tracker.habits:
    st.info("No habits added yet. Add some from the sidebar.")
else:
    for habit in st.session_state.tracker.habits:
        col1, col2 = st.columns([3, 1])
        with col1:
            done = st.checkbox(f"{habit.name} - Done today?", key=habit.name)
        with col2:
            if done:
                st.success("✅")
        habit.add_entry(done)

# Show Feedback
st.markdown("---")
st.subheader("📊 Your Progress")
st.markdown(st.session_state.tracker.get_burnout_risk())

suggestions = st.session_state.tracker.get_suggestions()
if suggestions:
    st.markdown("💡 Suggestions:")
    for tip in suggestions:
        st.markdown(f"- {tip}")
else:
    st.markdown("🎯 No suggestions needed right now!")

# Show Last 7 Days per Habit
st.markdown("### 📆 Last 7 Days Summary")
for habit in st.session_state.tracker.habits:
    recent = habit.last_7_days()
    st.write(f"**{habit.name}**: ", " ".join(["✅" if done else "❌" for done in recent]))

# Motivation
st.markdown("---")
st.subheader("💬 Daily Motivation")
st.info(get_random_quote())

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Python OOP")
