from nicegui import ui, app
import webview
import os
import asyncio
import datetime
import json

import ast
import doc_stat
from main import lint


class MyApp:

    def __init__(self):
        self.file_path = ""
        self.summary_text = None
        self.results_text = None

    async def pick_folder(self, file):
        directory_path = await app.native.main_window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
        directory_path = directory_path[0]
        if directory_path and os.path.exists(os.path.join(directory_path, "__init__.py")):
            self.file_path = directory_path
            self.results_text.text = f"Выбран проект: {directory_path}\n"
            self.display_analysis_history(self.file_path)
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
            warning_count = convention_count = refactor_count = 0
            for root, dirs, files in os.walk(directory_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        file_result, w, c, r = await self.lint_file(file_path)
                        new_text += file_result
                        warning_count += w
                        convention_count += c
                        refactor_count += r

            total_issues = warning_count + convention_count + refactor_count
            doc_percentage = doc_stat.calculate_documented_percentage(directory_path)
            timestamp = datetime.datetime.now().isoformat()

            summary = {
                "timestamp": timestamp,
                "doc_percentage": doc_percentage,
                "total_issues": total_issues,
                "warnings": warning_count,
                "convention": convention_count,
                "refactor": refactor_count
            }

            self.save_analysis_summary(directory_path, summary)

            sum_text = (f"Процент задокументированных классов и функций: {doc_percentage}%"
                        f"\n\nОбщее количество проблем: {total_issues}"
                        f"\n - Warnings: {warning_count}"
                        f"\n - Convention: {convention_count}"
                        f"\n - Refactor: {refactor_count}")
            self.summary_text.text = sum_text
            self.results_text.text = new_text

            self.display_analysis_history(self.file_path)
        except Exception as e:
            await ui.notify(f"Не удалось проанализировать проект: {str(e)}", type='error')

    async def lint_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            errors = lint(content)

            warning_count = convention_count = refactor_count = 0
            new_text = f"------------------------------------------------------------\nРезультаты для {file_path}:\n"
            if errors:
                for error in errors:
                    if error.startswith("E"):
                        warning_count += 1
                        error = error[1:]
                    elif error.startswith("C"):
                        convention_count += 1
                        error = error[1:]
                    elif error.startswith("R"):
                        refactor_count += 1
                        error = error[1:]
                    new_text += f"{error}\n\n"
            else:
                new_text += "Проблемы не найдены.\n\n"
            return new_text, warning_count, convention_count, refactor_count
        except Exception as e:
            await ui.notify(f"Не удалось проанализировать файл: {file_path}: {str(e)}", type='error')

    def save_analysis_summary(self, directory_path, summary):
        history_file = os.path.join(directory_path, '.analysis_history.json')
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as file:
                    history = json.load(file)
            else:
                history = []

            history.append(summary)
            with open(history_file, 'w') as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"Failed to save analysis summary: {str(e)}")


    def display_analysis_history(self, directory_path):
        history_file = os.path.join(directory_path, '.analysis_history.json')
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as file:
                    history = json.load(file)

                timestamps = [entry['timestamp'] for entry in history]
                total_issues = [entry['total_issues'] for entry in history]
                warnings = [entry['warnings'] for entry in history]
                conventions = [entry['convention'] for entry in history]
                refactors = [entry['refactor'] for entry in history]

                # Highcharts configuration
                options = {
                    'series': [
                        {'name': 'Total Issues', 'data': total_issues},
                        {'name': 'Warnings', 'data': warnings},
                        {'name': 'Conventions', 'data': conventions},
                        {'name': 'Refactors', 'data': refactors}
                    ]
                }

                if self.history_chart:
                    self.history_chart.options['series'] = options['series']
                    self.history_chart.update()
                else:
                    self.history_chart = ui.highchart(options).style('width: 100%; height: 400px')

        except Exception as e:
            print(f"Нет истории анализов: {str(e)}")

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

mapp = MyApp()

# with ui.card().style('background-color: #404252; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%'):
#     
#     with ui.row().style('gap: 10px; margin-top: 20px'):
#         ui.button('Выбор проекта', on_click=mapp.pick_folder).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')
#         ui.button('Анализ', on_click=mapp.analyze_directory).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')
#         ui.button('О программе', on_click=mapp.show_about).style('background-color: #282a3a; color: white; font-size: 16px; height: 30px')

#     # Analysis Summary
#     with ui.card().style('background-color: #b3b5bd; width: 100%; margin-top: 20px; padding: 20px; border-radius: 10px'):
#         ui.label('Результаты анализа').style('font-family: Helvetica; font-size: 14px; font-weight: bold; margin-bottom: 10px')
#         mapp.summary_text = ui.label('').style('background-color: #282a3a; white-space: pre-wrap; color: #f3f4f8; padding: 10px; border-radius: 5px; margin-bottom: 20px; width: 100%')

#     # Detailed Results
#     with ui.card().style('background-color: #b3b5bd; width: 100%; height: 200px; margin-top: 20px; padding: 20px; border-radius: 10px; overflow: auto'):
#         mapp.results_text = ui.label('\n\n\n\n\n').style('background-color: #282a3a; white-space: pre-wrap; color: #f3f4f8; padding: 5px; border-radius: 5px; width: 100%; height: 100%')

with ui.card().style('background-color: #f0f0f5; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%'):
    
    with ui.row().style('gap: 10px; margin-top: 20px'):
        ui.button('Выбор проекта', on_click=mapp.pick_folder).style('background-color: #4CAF50; color: white; font-size: 16px; height: 40px')
        ui.button('Анализ', on_click=mapp.analyze_directory).style('background-color: #2196F3; color: white; font-size: 16px; height: 40px')
        ui.button('О программе', on_click=mapp.show_about).style('background-color: #FFC107; color: white; font-size: 16px; height: 40px')

    # Analysis Summary
    with ui.row().style('gap: 10px; width: 100%; margin-top: 20px'):
        with ui.card().style('background-color: #e0e0eb; padding: 20px; border-radius: 10px; flex: 1'):
            ui.label('Результаты анализа').style('font-family: Helvetica; font-size: 14px; font-weight: bold; margin-bottom: 10px')
            mapp.summary_text = ui.label('').style('background-color: #f8f8f8; white-space: pre-wrap; color: #333; padding: 10px; border-radius: 5px; width: 100%')

    # Detailed Results
    with ui.row().style('gap: 10px; width: 100%; margin-top: 20px'):
        with ui.card().style('background-color: #e0e0eb; padding: 20px; border-radius: 10px; flex: 1; overflow: auto; height: 200px'):
            ui.label('Детализированные результаты').style('font-family: Helvetica; font-size: 14px; font-weight: bold; margin-bottom: 10px')
            mapp.results_text = ui.label('\n\n\n\n\n').style('background-color: #f8f8f8; white-space: pre-wrap; color: #333; padding: 5px; border-radius: 5px; width: 100%; height: 100%')

    options = {
        'chart': {'type': 'line'},
        'title': {'text': 'История результатов анализа'},
        'yAxis': {'title': {'text': 'Количество проблем'}},
        'series': [
            {'name': 'Total Issues', 'data': []},
            {'name': 'Warnings', 'data': []},
            {'name': 'Conventions', 'data': []},
            {'name': 'Refactors', 'data': []}
        ]
    }
    # Charts Placeholder
    with ui.row().style('background-color: #e0e0eb; width: 100%; padding: 20px; border-radius: 10px; flex: 1'):
        ui.label('История результатов анализа').style('font-family: Helvetica; font-size: 14px; font-weight: bold; color: white; margin-bottom: 10px')
    # with ui.row().style('gap: 10px; width: 100%; margin-top: 20px'):
        # ui.label('История результатов анализа').style('font-family: Helvetica; font-size: 12px; font-style: italic; color: white')
        mapp.history_chart = ui.highchart(options).style('width: 100%; height: 400px')

ui.run(native=True, reload=False, window_size=(1200, 1000))
