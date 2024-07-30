import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThermalExpansionCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Thermal Expansion Calculator v1.1")

        self.components = [
            {"name": "Sleeve", "color": "orange"},
            {"name": "Solder", "color": "green"},
            {"name": "Backing Tube", "color": "blue"}
        ]
        
        for component in self.components:
            component.update({
                'outer_diameter': tk.DoubleVar(value=100),
                'inner_diameter': tk.DoubleVar(value=90),
                'cte': tk.DoubleVar(value=1e-5),
                'temperature': tk.DoubleVar(value=25)
            })

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        input_frame = ttk.Frame(self.master)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i, component in enumerate(self.components):
            frame = ttk.LabelFrame(input_frame, text=component['name'])
            frame.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            labels = ["Outer Diameter (mm):", "Inner Diameter (mm):", "CTE (1/°C):", "Temperature (°C):"]
            vars = ['outer_diameter', 'inner_diameter', 'cte', 'temperature']

            for j, (label, var) in enumerate(zip(labels, vars)):
                ttk.Label(frame, text=label).grid(row=j, column=0, sticky="w")
                if var != 'temperature':
                    ttk.Entry(frame, textvariable=component[var], width=10).grid(row=j, column=1)
                else:
                    temp_scale = ttk.Scale(frame, from_=25, to=250, variable=component[var], 
                                           orient="horizontal", command=self.update_plot)
                    temp_scale.grid(row=j, column=1, sticky="ew")
                    ttk.Label(frame, textvariable=component[var]).grid(row=j, column=2)
                component[var].trace_add('write', self.update_plot)

        # Create side table for actual dimensions
        self.side_table = ttk.Treeview(self.master, columns=('Component', 'Temperature', 'Outer Diameter', 'Inner Diameter'), show='headings')
        self.side_table.heading('Component', text='Component')
        self.side_table.heading('Temperature', text='Temp (°C)')
        self.side_table.heading('Outer Diameter', text='Outer Diameter (mm)')
        self.side_table.heading('Inner Diameter', text='Inner Diameter (mm)')
        self.side_table.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
        self.update_plot()

    def update_plot(self, *args):
        self.ax.clear()
        max_diameter = 0

        # Clear existing items in the side table
        for item in self.side_table.get_children():
            self.side_table.delete(item)

        for component in self.components:
            outer_diameter = component['outer_diameter'].get()
            inner_diameter = component['inner_diameter'].get()
            cte = component['cte'].get()
            temperature = component['temperature'].get()

            new_outer_diameter = outer_diameter * (1 + cte * (temperature - 25))
            new_inner_diameter = inner_diameter * (1 + cte * (temperature - 25))

            max_diameter = max(max_diameter, new_outer_diameter)

            # Outer circle
            self.ax.add_patch(plt.Circle((0, 0), new_outer_diameter/2, 
                                         fill=False, edgecolor=component['color'], linewidth=2))
            # Inner circle
            self.ax.add_patch(plt.Circle((0, 0), new_inner_diameter/2, 
                                         fill=False, edgecolor=component['color'], linewidth=2))

            # Update side table
            self.side_table.insert('', 'end', values=(component['name'], f'{temperature:.1f}', f'{new_outer_diameter:.2f}', f'{new_inner_diameter:.2f}'))

        # Set limits and aspect
        limit = max_diameter * 0.6
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.axis('off')
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = ThermalExpansionCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
