from nicegui import ui
import os
import asyncio

import ast
import doc_stat
from main import lint

class MyApp:

    def __init__(self):
        self.file_path = ""
        self.summary_text = None
        self.results_text = None

    async def pick_folder(self):
        directory_path = await ui.open_directory()
        if directory_path and os.path.exists(os.path.join(directory_path, "__init__.py")):
            self.file_path = directory_path
            self.results_text.text = f"Выбран проект: {directory_path}\n"
        else:
            self.results_text.text = f"Не удалось выбрать проект {directory_path}. Удостоверьтесь, что в проекте есть __init__.py.\n"

    async def analyze_directory(self):
        directory_path = self.file_path
        if not directory_path:
            await ui.notify("Проект не выбран. Укажите проект, который должен быть проанализирован.", type='warning')
            return

        try:
            self.results_text.text = f"Проводится анализ проекта: {directory_path}\n"
            new_text = ""
            for root, dirs, files in os.walk(directory_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        new_text += await self.lint_file(file_path)
            self.results_text.text = new_text
            doc_percentage = doc_stat.calculate_documented_percentage(directory_path)
            sum_text = (f"Процент задокументированных классов и функций: {doc_percentage}%"
                        "\n\nОбщее количество проблем:"
                        "\n - Warnings:"
                        "\n - Convention:"
                        "\n - Refactor:")
            self.summary_text.text = sum_text
        except Exception as e:
            await ui.notify(f"Не удалось проанализировать проект: {str(e)}", type='error')

    async def lint_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            errors = lint(content)

            new_text = f"------------------------------------------------------------\nРезультаты для {file_path}:\n"
            if errors:
                for error in errors:
                    new_text += f"{error}\n\n"
            else:
                new_text += "Проблемы не найдены.\n\n"
            return new_text
        except Exception as e:
            await ui.notify(f"Не удалось проанализировать файл: {file_path}: {str(e)}", type='error')

    async def save_result(self):
        result_text = self.results_text.text
        if not result_text.strip():
            await ui.notify("No Result. There is no result to save.", type='warning')
            return

        file_path = await ui.open_file_dialog(save=True, file_extensions=['.txt'])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(result_text)
                await ui.notify("Results saved successfully.", type='info')
            except Exception as e:
                await ui.notify(f"Failed to save results: {str(e)}", type='error')

    async def show_about(self):
        await ui.notify("Это программа для анализа кода. Укажите проект и проанализируйте его с помощью кнопок в интерфейсе.\n Разработчик: Камелов Н.Н.", type='info')

app = MyApp()

with ui.card().style('background-color: #404252; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center'):
    
    with ui.card().style('background-color: #404252; display: flex; justify-content: center; width: 100%'):
        with ui.row().style('gap: 10px'):
            ui.button('Выбор проекта', on_click=app.pick_folder).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')
            ui.button('Анализ', on_click=app.analyze_directory).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')
            ui.button('О программе', on_click=app.show_about).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')

    with ui.card().style('background-color: #b3b5bd; width: 80%; margin-top: 20px; padding: 20px; border-radius: 10px'):
        ui.label('Результаты анализа').style('font-family: Helvetica; font-size: 14px; font-weight: bold; margin-bottom: 10px')
        app.summary_text = ui.label('').style('background-color: #282a3a; color: #f3f4f8; padding: 10px; border-radius: 5px; margin-bottom: 20px')

    with ui.card().style('background-color: #b3b5bd; width: 80%; height: 200px; margin-top: 20px; padding: 20px; border-radius: 10px; overflow: auto'):
        app.results_text = ui.label('\n\n\n\n\n').style('background-color: #282a3a; color: #f3f4f8; padding: 5px; border-radius: 5px; width: 100%; height: 100%')

    with ui.card().style('background-color: #404252; width: 80%; margin-top: 20px; padding: 20px; border-radius: 10px'):
        ui.label('История результатов анализа:\n[Charts Placeholder]').style('font-family: Helvetica; font-size: 12px; font-style: italic; color: white')

ui.run()
