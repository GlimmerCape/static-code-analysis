import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter
import os

import ast
import doc_stat
from main import lint

CODE = ""


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Инструмент для статического анализа кода")

        # Main Frame
        # main_frame = customtkinter.CTkFrame(root, width=800, height=600, fg_color="#404252")
        main_frame = customtkinter.CTkFrame(root, fg_color="#404252")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Button Frame
        button_frame_out = customtkinter.CTkFrame(main_frame, fg_color="#404252")
        button_frame_out.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        button_frame = customtkinter.CTkFrame(button_frame_out, height=100, fg_color="#404252")
        button_frame.pack(expand=True)

        button_frame.columnconfigure(0, weight=1, uniform="a")
        button_frame.columnconfigure(1, weight=1, uniform="a")
        button_frame.columnconfigure(2, weight=1, uniform="a")
        button_frame.columnconfigure(3, weight=1, uniform="a")
        self.file_path = tk.StringVar()
        self.file_button = customtkinter.CTkButton(button_frame, text="Выбор проекта", font=("Verdana", 16), height=30, command=self.pick_folder, fg_color="#282a3a")
        self.file_button.grid(row=0, column=1, padx=5, pady=5)

        self.analyze_button = customtkinter.CTkButton(button_frame, text="Анализ", font=("Verdana", 16), height=30, command=self.analyze_directory, fg_color="#282a3a")
        self.analyze_button.grid(row=0, column=2, padx=5, pady=5)

        self.about_button = customtkinter.CTkButton(button_frame, text="О программе", font=("Verdana", 16), height=30, command=self.show_about, fg_color="#282a3a")
        self.about_button.grid(row=0, column=3, padx=5, pady=5)

        # Analysis Summary
        summary_frame = customtkinter.CTkFrame(main_frame, fg_color="#b3b5bd")
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        summary_label = customtkinter.CTkLabel(summary_frame, text="Результаты анализа", font=("Helvetica", 14, "bold"))
        summary_label.pack(expand=True)
        
        self.summary_text = customtkinter.CTkLabel(summary_frame, text="", bg_color="#282a3a", text_color="#f3f4f8", anchor="w", justify="left", width=760, height=100, padx=10, pady=10)
        self.summary_text.pack(expand=True, pady=2, padx=2)

        # Detailed Results
        results_frame = customtkinter.CTkScrollableFrame(main_frame, fg_color="#b3b5bd", height=200)
        results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.results_text = customtkinter.CTkLabel(results_frame, bg_color="#282a3a", text_color="#f3f4f8", anchor="nw", justify="left", width=760, height=200, padx=5, pady=5, wraplength=750, text="\n\n\n\n\n")
        self.results_text.grid(sticky="nsew", pady=2, padx=2)
        
        # Error Distribution (Placeholder for Charts)
        charts_frame = customtkinter.CTkFrame(main_frame)
        charts_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        chart_placeholder = customtkinter.CTkLabel(charts_frame, text="История результатов анализа:\n[Charts Placeholder]", font=("Helvetica", 12, "italic"))
        chart_placeholder.grid(row=0, column=0, sticky="ew")
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        # # Main Frame
        # main_frame = customtkinter.CTkFrame(root, width=800, height=600)
        # main_frame.grid(row=0, column=0, sticky="nsew")

        # # Button Frame
        # button_frame = customtkinter.CTkFrame(main_frame)
        # button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # self.file_path = tk.StringVar()
        # self.file_button = customtkinter.CTkButton(button_frame, text="Select Project", command=self.pick_folder)
        # self.file_button.grid(row=0, column=0, padx=5, pady=5)

        # self.analyze_button = customtkinter.CTkButton(button_frame, text="Analyze", command=self.analyze_directory)
        # self.analyze_button.grid(row=0, column=1, padx=5, pady=5)

        # # Analysis Summary
        # summary_frame = customtkinter.CTkFrame(main_frame)
        # summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # 
        # summary_label = customtkinter.CTkLabel(summary_frame, text="Analysis Summary:")
        # summary_label.grid(row=0, column=0, sticky="w")
        # 
        # self.summary_text = customtkinter.CTkTextbox(summary_frame, wrap=tk.WORD, width=760, height=100)
        # self.summary_text.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # # Detailed Results
        # results_frame = customtkinter.CTkFrame(main_frame)
        # results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # results_label = customtkinter.CTkLabel(results_frame, text="Detailed Results:")
        # results_label.grid(row=0, column=0, sticky="w")

        # self.results_text = customtkinter.CTkTextbox(results_frame, wrap=tk.WORD, width=760, height=200)
        # self.results_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        # 
        # # Error Distribution (Placeholder for Charts)
        # charts_frame = customtkinter.CTkFrame(main_frame)
        # charts_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        # 
        # chart_placeholder = customtkinter.CTkLabel(charts_frame, text="Error Distribution:\n[Charts Placeholder]")
        # chart_placeholder.grid(row=0, column=0, sticky="ew")
        # 
        # main_frame.columnconfigure(0, weight=1)
        # main_frame.rowconfigure(2, weight=1)

    def pick_folder(self):
        directory_path = filedialog.askdirectory()
        if directory_path and os.path.exists(os.path.join(directory_path, "__init__.py")):
            self.file_path.set(directory_path)
            self.results_text.configure(text=f"Выбран проект: {directory_path}\n")
        else:
            self.results_text.configure(text=f"Не удалось выбрать проект{directory_path}. Удостоверьтесь что в проекте есть __init__.py.\n")

    def analyze_directory(self):
        directory_path = self.file_path.get()
        if not directory_path:
            messagebox.showwarning("Проект не выбран", "Укажите проект, который должен быть проанализирован.")
            return
        try:
            self.results_text.configure(text=f"Проводится анализ проекта: {directory_path}\n")
            new_text = ""
            for root, dirs, files in os.walk(directory_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        new_text = new_text + self.lint_file(file_path)
            self.results_text.configure(text=new_text)
            sum_text = f"Процент задокументированных классов и функций: {doc_stat.calculate_documented_percentage(directory_path)}%"

            sum_text = sum_text + "\n\n Общее количество проблем:"
            sum_text = sum_text + "\n - Warnings:"
            sum_text = sum_text + "\n - Convention:"
            sum_text = sum_text + "\n - Refactor:"
            self.summary_text.configure(text=sum_text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проанализировать проект: {str(e)}")

    def lint_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            errors = lint(content)

            new_text = ""
            new_text = new_text = f"------------------------------------------------------------\nРезультаты для {file_path}:\n"
            if errors:
                for error in errors:
                    new_text = new_text + f"{error}\n\n"
            else:
                new_text = new_text + "Проблемы не найдены.\n\n"
            return new_text
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проанализировать файл: {file_path}: {str(e)}")

    def save_result(self):
        result_text = self.results_text.get("1.0", tk.END)
        if not result_text.strip():
            messagebox.showwarning("No Result", "There is no result to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(result_text)
                messagebox.showinfo("Saved", "Results saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    def show_about(self):
        messagebox.showinfo("О программе", "Это программа для анализа кода. Укажите проект и проанализируйте его с помощью кнопок в интерфейсе.\n Разработчик: Камелов Н.Н.")


if __name__ == "__main__":
    def close_window(event):
        root.quit()

    root = customtkinter.CTk()
    root.bind('<Control-w>', close_window)
    root.bind('<Control-q>', close_window)
    app = CodeAnalyzerApp(root)
    root.maxsize(800, 800)
    root.mainloop()
