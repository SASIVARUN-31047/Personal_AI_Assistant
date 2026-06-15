from voice import listen
from speak import speak
from tasks import init_db, add_task, get_tasks, clear_tasks
from reminders import set_reminder
import time

WAKE_WORD = "jarvis"

init_db()
speak("Assistant sleeping. Say jarvis to wake me up.")

while True:
    wake = listen()
    print("Wake heard:", wake)

    if WAKE_WORD in wake:
        speak("Yes, how can I help you?")
        command = listen()
        print("Command:", command)

        if not command:
            speak("I didn't hear anything")
            continue

        if "exit" in command:
            speak("Goodbye")
            break

        elif "add task" in command:
            task = command.replace("add task", "").strip()
            add_task(task)
            speak("Task added")

        elif "show tasks" in command:
            tasks = get_tasks()
            if not tasks:
                speak("You have no tasks")
            else:
                speak("Your tasks are")
                for t in tasks:
                    speak(t)

        elif "clear tasks" in command:
            clear_tasks()
            speak("All tasks cleared")

        elif "remind me" in command:
            speak("What should I remind you about?")
            task = listen()
            speak("At what time? Say like 18 30")
            time_str = listen().replace(" ", ":")
            set_reminder(task, time_str)
            speak("Reminder set")

        else:
            speak("I did not understand that")

        speak("Going back to sleep")
