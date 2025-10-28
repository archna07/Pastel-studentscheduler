import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta
import time
import threading
import random
import winsound

class PastelStudentScheduler:
    def __init__(self, root):
        self.root = root
        self.schedule_data = []
        self.current_timers = []
        self.motivational_quotes = self.load_quotes()
        
        # Initialize variables
        self.task_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="45")
        self.priority_var = tk.StringVar(value="Medium")
        self.timer_var = tk.StringVar(value="25")
        self.progress_var = tk.StringVar(value="0%")
        
        # Pastel color palette
        self.colors = {
            'bg': '#fafafa',
            'card': '#ffffff',
            'primary': '#a8d8ea',      # Soft blue
            'secondary': '#aa96da',    # Soft purple
            'accent': '#ffd3b6',       # Soft peach
            'success': '#c7ecee',      # Mint
            'warning': '#ffaaa5',      # Soft coral
            'text': '#2d3436',         # Dark gray
            'border': '#dfe6e9'        # Light gray
        }
        
        self.setup_ui()
        self.start_clock()
        
    def load_quotes(self):
        return [
            "Small steps every day lead to big achievements",
            "Your focus determines your reality",
            "Progress, not perfection",
            "The expert in anything was once a beginner",
            "You are capable of amazing things",
            "Consistency is the key to mastery",
            "Every minute spent planning saves ten in execution",
            "Your future self will thank you",
            "Quality over quantity in learning",
            "Rest is part of the process",
            "Mindful studying beats rushed cramming",
            "Balance is the secret to sustainability"
        ]
    
    def setup_ui(self):
        self.root.title("Student Scheduler")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['bg'])
        
        # Create main frames with minimal borders
        self.create_header()
        self.create_main_layout()
        
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Student Scheduler", 
                              font=('Arial', 20, 'bold'), 
                              bg=self.colors['primary'], 
                              fg=self.colors['text'])
        title_label.pack(pady=20)
        
    def create_main_layout(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Left panel - Input and schedule
        left_panel = tk.Frame(main_container, bg=self.colors['bg'])
        left_panel.pack(side='left', fill='both', expand=True)
        
        # Right panel - Visualizations and motivation
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_input_section(left_panel)
        self.create_schedule_section(left_panel)
        self.create_timer_section(right_panel)
        self.create_visualization_section(right_panel)
        self.create_motivation_section(right_panel)
    
    def create_input_section(self, parent):
        input_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', 
                              highlightbackground=self.colors['border'], 
                              highlightthickness=1)
        input_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(input_frame, text="Add Study Session", 
                font=('Arial', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=10)
        
        # Input fields
        fields_frame = tk.Frame(input_frame, bg=self.colors['card'])
        fields_frame.pack(fill='x', padx=15, pady=5)
        
        # Task
        self.create_input_field(fields_frame, "Subject:", 0, self.task_var)
        
        # Duration
        self.create_input_field(fields_frame, "Duration (min):", 1, self.duration_var)
        
        # Priority
        tk.Label(fields_frame, text="Priority:", bg=self.colors['card'],
                font=('Arial', 9)).grid(row=2, column=0, sticky='w', pady=5)
        priority_combo = ttk.Combobox(fields_frame, textvariable=self.priority_var,
                                    values=["High", "Medium", "Low"], width=15)
        priority_combo.grid(row=2, column=1, pady=5, padx=5, sticky='w')
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=10)
        
        buttons = [
            ("Add Session", self.add_session, self.colors['secondary']),
            ("Water Break", self.add_water_break, self.colors['success']),
            ("Food Break", self.add_food_break, self.colors['accent']),
            ("Clear All", self.clear_schedule, self.colors['warning'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                          bg=color, fg=self.colors['text'], font=('Arial', 9),
                          relief='flat', padx=10)
            btn.pack(side='left', padx=5)
    
    def create_input_field(self, parent, label, row, variable):
        tk.Label(parent, text=label, bg=self.colors['card'],
                font=('Arial', 9)).grid(row=row, column=0, sticky='w', pady=5)
        entry = tk.Entry(parent, textvariable=variable, width=20,
                        font=('Arial', 9), relief='flat',
                        highlightbackground=self.colors['border'],
                        highlightthickness=1)
        entry.grid(row=row, column=1, pady=5, padx=5, sticky='w')
    
    def create_schedule_section(self, parent):
        schedule_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat',
                                 highlightbackground=self.colors['border'], 
                                 highlightthickness=1)
        schedule_frame.pack(fill='both', expand=True)
        
        tk.Label(schedule_frame, text="Today's Schedule", 
                font=('Arial', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=10)
        
        # Treeview for schedule
        columns = ("Time", "Task", "Duration", "Priority")
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=columns, 
                                         show="headings", height=10)
        
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=80)
        
        self.schedule_tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", 
                                 command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
    
    def create_timer_section(self, parent):
        timer_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat',
                              highlightbackground=self.colors['border'], 
                              highlightthickness=1)
        timer_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(timer_frame, text="Timer & Alarms", 
                font=('Arial', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=10)
        
        # Current time
        self.time_label = tk.Label(timer_frame, text="", 
                                  font=('Arial', 16, 'bold'),
                                  bg=self.colors['card'], 
                                  fg=self.colors['text'])
        self.time_label.pack(pady=5)
        
        # Timer controls
        control_frame = tk.Frame(timer_frame, bg=self.colors['card'])
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Timer (min):", bg=self.colors['card'],
                font=('Arial', 9)).pack(side='left', padx=5)
        
        timer_spin = tk.Spinbox(control_frame, from_=1, to=120, 
                               textvariable=self.timer_var, width=8,
                               font=('Arial', 9))
        timer_spin.pack(side='left', padx=5)
        
        timer_btn = tk.Button(control_frame, text="Start Timer", 
                             command=self.start_timer,
                             bg=self.colors['primary'], 
                             fg=self.colors['text'],
                             font=('Arial', 9), relief='flat')
        timer_btn.pack(side='left', padx=5)
        
        # Active timer display
        self.timer_display = tk.Label(timer_frame, text="No active timers", 
                                     font=('Arial', 10), 
                                     bg=self.colors['card'], 
                                     fg=self.colors['text'])
        self.timer_display.pack(pady=5)
    
    def create_visualization_section(self, parent):
        viz_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat',
                            highlightbackground=self.colors['border'], 
                            highlightthickness=1)
        viz_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(viz_frame, text="Study Analytics", 
                font=('Arial', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=10)
        
        # Create minimal matplotlib figure
        plt.rcParams['font.size'] = 9
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 3))
        self.fig.patch.set_facecolor(self.colors['card'])
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor(self.colors['card'])
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)
        
        self.update_visualizations()
    
    def create_motivation_section(self, parent):
        mot_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat',
                            highlightbackground=self.colors['border'], 
                            highlightthickness=1)
        mot_frame.pack(fill='x')
        
        tk.Label(mot_frame, text="Daily Motivation", 
                font=('Arial', 12, 'bold'), 
                bg=self.colors['card'], 
                fg=self.colors['text']).pack(pady=10)
        
        # Motivational quote
        self.quote_label = tk.Label(mot_frame, text="", 
                                   font=('Arial', 10, 'italic'),
                                   bg=self.colors['card'], 
                                   fg=self.colors['text'],
                                   wraplength=400, justify='center')
        self.quote_label.pack(pady=10, padx=10)
        
        # Progress
        progress_frame = tk.Frame(mot_frame, bg=self.colors['card'])
        progress_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(progress_frame, text="Today's Progress:", 
                bg=self.colors['card'], font=('Arial', 9)).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', 
                                          length=300, mode='determinate')
        self.progress_bar.pack(fill='x', pady=5)
        
        self.progress_label = tk.Label(progress_frame, 
                                     textvariable=self.progress_var,
                                     bg=self.colors['card'], 
                                     font=('Arial', 9))
        self.progress_label.pack()
        
        # New quote button
        quote_btn = tk.Button(mot_frame, text="New Motivation", 
                             command=self.new_motivation,
                             bg=self.colors['accent'], 
                             fg=self.colors['text'],
                             font=('Arial', 9), relief='flat')
        quote_btn.pack(pady=10)
        
        self.new_motivation()
    
    def start_clock(self):
        def update_time():
            while True:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.time_label.config(text=current_time)
                time.sleep(1)
        
        clock_thread = threading.Thread(target=update_time, daemon=True)
        clock_thread.start()
    
    def add_session(self):
        task = self.task_var.get().strip()
        duration = self.duration_var.get().strip()
        
        if not task or not duration:
            messagebox.showwarning("Input Error", "Please enter subject and duration")
            return
        
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid duration")
            return
        
        start_time = self.calculate_start_time()
        end_time = start_time + timedelta(minutes=duration)
        
        session = {
            'start': start_time,
            'end': end_time,
            'task': task,
            'duration': duration,
            'priority': self.priority_var.get(),
            'category': 'Study'
        }
        
        self.schedule_data.append(session)
        self.update_schedule_display()
        self.update_visualizations()
        self.update_progress()
        
        self.task_var.set("")
    
    def add_water_break(self):
        self.task_var.set("Water Break")
        self.duration_var.set("5")
        self.priority_var.set("High")
        self.add_session()
    
    def add_food_break(self):
        self.task_var.set("Food Break")
        self.duration_var.set("30")
        self.priority_var.set("High")
        self.add_session()
    
    def calculate_start_time(self):
        if not self.schedule_data:
            return datetime.now().replace(second=0, microsecond=0)
        
        last_session = max(self.schedule_data, key=lambda x: x['end'])
        return last_session['end']
    
    def update_schedule_display(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        sorted_schedule = sorted(self.schedule_data, key=lambda x: x['start'])
        for session in sorted_schedule:
            start_str = session['start'].strftime("%H:%M")
            self.schedule_tree.insert("", "end", values=(
                start_str,
                session['task'],
                f"{session['duration']} min",
                session['priority']
            ))
    
    def update_visualizations(self):
        self.ax1.clear()
        self.ax2.clear()
        
        if not self.schedule_data:
            self.ax1.text(0.5, 0.5, 'Add study sessions\nto see analytics', 
                         ha='center', va='center', transform=self.ax1.transAxes,
                         fontsize=10, color=self.colors['text'])
            self.ax2.text(0.5, 0.5, 'Add study sessions\nto see analytics', 
                         ha='center', va='center', transform=self.ax2.transAxes,
                         fontsize=10, color=self.colors['text'])
        else:
            # Time distribution
            categories = {}
            for session in self.schedule_data:
                cat = session['category']
                duration = session['duration']
                categories[cat] = categories.get(cat, 0) + duration
            
            # Pastel colors for pie chart
            pastel_colors = [self.colors['primary'], self.colors['secondary'], 
                           self.colors['accent'], self.colors['success']]
            
            self.ax1.pie(categories.values(), labels=categories.keys(), 
                        autopct='%1.0f%%', colors=pastel_colors[:len(categories)],
                        startangle=90, textprops={'color': self.colors['text']})
            self.ax1.set_title('Time Distribution', color=self.colors['text'])
            
            # Daily timeline
            for i, session in enumerate(sorted(self.schedule_data, key=lambda x: x['start'])):
                start = session['start']
                duration = session['duration']
                
                color_map = {
                    'Study': self.colors['primary'],
                    'Water Break': self.colors['success'],
                    'Food Break': self.colors['accent']
                }
                
                color = color_map.get(session['task'], self.colors['secondary'])
                
                self.ax2.barh(i, duration, left=start.hour + start.minute/60, 
                             color=color, alpha=0.8)
        
        self.ax2.set_yticks(range(len(self.schedule_data)))
        self.ax2.set_yticklabels([s['task'] for s in sorted(self.schedule_data, key=lambda x: x['start'])])
        self.ax2.set_xlabel('Time of Day', color=self.colors['text'])
        self.ax2.set_title('Daily Schedule', color=self.colors['text'])
        self.ax2.tick_params(colors=self.colors['text'])
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def update_progress(self):
        total_study_time = sum(session['duration'] for session in self.schedule_data 
                             if session['category'] == 'Study')
        
        max_study_time = 6 * 60  # 6 hours target
        progress_percent = min(100, (total_study_time / max_study_time) * 100)
        
        self.progress_bar['value'] = progress_percent
        self.progress_var.set(f"{progress_percent:.0f}%")
    
    def start_timer(self):
        try:
            minutes = int(self.timer_var.get())
            if minutes <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid minutes")
            return
        
        end_time = datetime.now() + timedelta(minutes=minutes)
        timer_id = len(self.current_timers)
        
        timer_data = {
            'id': timer_id,
            'end_time': end_time,
            'duration': minutes,
            'active': True
        }
        
        self.current_timers.append(timer_data)
        
        timer_thread = threading.Thread(target=self.run_timer, args=(timer_id,), daemon=True)
        timer_thread.start()
        
        self.update_timer_display()
        messagebox.showinfo("Timer Started", f"Timer set for {minutes} minutes")
    
    def run_timer(self, timer_id):
        timer_data = next((t for t in self.current_timers if t['id'] == timer_id), None)
        if not timer_data:
            return
        
        while datetime.now() < timer_data['end_time'] and timer_data['active']:
            time.sleep(1)
        
        if timer_data['active']:
            self.trigger_alarm(f"Timer completed! {timer_data['duration']} minutes elapsed.")
            self.current_timers = [t for t in self.current_timers if t['id'] != timer_id]
            self.update_timer_display()
    
    def update_timer_display(self):
        if not self.current_timers:
            self.timer_display.config(text="No active timers")
        else:
            timer_text = "Active timers:\n"
            for timer in self.current_timers:
                if timer['active']:
                    remaining = timer['end_time'] - datetime.now()
                    minutes = int(remaining.total_seconds() // 60)
                    seconds = int(remaining.total_seconds() % 60)
                    timer_text += f"{minutes:02d}:{seconds:02d} remaining\n"
            
            self.timer_display.config(text=timer_text)
    
    def trigger_alarm(self, message):
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except:
            pass
        
        messagebox.showinfo("Alarm", message)
    
    def new_motivation(self):
        quote = random.choice(self.motivational_quotes)
        self.quote_label.config(text=quote)
    
    def clear_schedule(self):
        if messagebox.askyesno("Clear Schedule", "Clear entire schedule?"):
            self.schedule_data.clear()
            self.update_schedule_display()
            self.update_visualizations()
            self.update_progress()

def main():
    root = tk.Tk()
    app = PastelStudentScheduler(root)
    root.mainloop()

if __name__ == "__main__":
    main()