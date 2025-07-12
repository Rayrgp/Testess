from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.popup import Popup
from kivy.core.window import Window

import json
import os
from datetime import datetime
import webbrowser
from urllib.parse import urlencode

class TaskItem(BoxLayout):
    def __init__(self, task_data, on_toggle, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.padding = [10, 5]
        
        self.task_data = task_data
        
        # Checkbox
        self.checkbox = Button(
            text='☐' if not task_data['completed'] else '☑',
            size_hint_x=0.1,
            on_press=lambda x: on_toggle(task_data['id'])
        )
        
        # Task title
        self.title_label = Label(
            text=task_data['title'],
            size_hint_x=0.7,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        if task_data['completed']:
            self.title_label.text = f"[s]{task_data['title']}[/s]"
        
        # Delete button
        self.delete_btn = Button(
            text='🗑',
            size_hint_x=0.2,
            on_press=lambda x: on_delete(task_data['id'])
        )
        
        self.add_widget(self.checkbox)
        self.add_widget(self.title_label)
        self.add_widget(self.delete_btn)

class NoteItem(BoxLayout):
    def __init__(self, note_data, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 120
        self.padding = [10, 5]
        
        # Note header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        title = Label(text=note_data['title'], size_hint_x=0.7, halign='left')
        delete_btn = Button(
            text='🗑',
            size_hint_x=0.3,
            on_press=lambda x: on_delete(note_data['id'])
        )
        header.add_widget(title)
        header.add_widget(delete_btn)
        
        # Note content
        content = Label(
            text=note_data['content'],
            size_hint_y=0.5,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        
        # Note date
        date = Label(
            text=note_data['created_at'][:10],
            size_hint_y=0.2,
            halign='left'
        )
        
        self.add_widget(header)
        self.add_widget(content)
        self.add_widget(date)

class UniversalApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = 'app_data.json'
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {'tasks': [], 'notes': []}
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def build(self):
        # Main layout
        main_layout = TabbedPanel()
        main_layout.default_tab_text = 'Início'
        
        # Home Tab
        home_tab = TabbedPanelItem(text='🏠 Início')
        home_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        welcome_label = Label(
            text='Bem-vindo ao App Universal!',
            size_hint_y=0.2,
            font_size='20sp'
        )
        
        desc_label = Label(
            text='Aplicativo móvel criado com Python Kivy\nFunciona offline e salva dados localmente',
            size_hint_y=0.3,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        home_layout.add_widget(welcome_label)
        home_layout.add_widget(desc_label)
        home_tab.add_widget(home_layout)
        
        # Tasks Tab
        tasks_tab = TabbedPanelItem(text='📋 Tarefas')
        tasks_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Task input
        task_input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.task_input = TextInput(
            hint_text='Digite sua tarefa...',
            multiline=False,
            size_hint_x=0.7
        )
        add_task_btn = Button(
            text='+',
            size_hint_x=0.3,
            on_press=self.add_task
        )
        task_input_layout.add_widget(self.task_input)
        task_input_layout.add_widget(add_task_btn)
        
        # Tasks list
        self.tasks_scroll = ScrollView(size_hint_y=0.9)
        self.tasks_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        
        tasks_layout.add_widget(task_input_layout)
        tasks_layout.add_widget(self.tasks_scroll)
        self.tasks_scroll.add_widget(self.tasks_layout)
        tasks_tab.add_widget(tasks_layout)
        
        # Notes Tab
        notes_tab = TabbedPanelItem(text='📝 Notas')
        notes_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Note input
        note_title_input = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.note_title = TextInput(
            hint_text='Título da nota...',
            multiline=False,
            size_hint_x=0.7
        )
        add_note_btn = Button(
            text='+',
            size_hint_x=0.3,
            on_press=self.add_note
        )
        note_title_input.add_widget(self.note_title)
        note_title_input.add_widget(add_note_btn)
        
        self.note_content = TextInput(
            hint_text='Conteúdo da nota...',
            multiline=True,
            size_hint_y=0.2
        )
        
        # Notes list
        self.notes_scroll = ScrollView(size_hint_y=0.7)
        self.notes_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        
        notes_layout.add_widget(note_title_input)
        notes_layout.add_widget(self.note_content)
        notes_layout.add_widget(self.notes_scroll)
        self.notes_scroll.add_widget(self.notes_layout)
        notes_tab.add_widget(notes_layout)
        
        # Apps Tab
        apps_tab = TabbedPanelItem(text='🔗 Apps')
        apps_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        qacademico_btn = Button(
            text='🎓 Q-Acadêmico IFF\nAcessar sistema acadêmico',
            size_hint_y=0.3,
            on_press=self.open_qacademico
        )
        
        apps_layout.add_widget(qacademico_btn)
        apps_tab.add_widget(apps_layout)
        
        # Add tabs
        main_layout.add_widget(home_tab)
        main_layout.add_widget(tasks_tab)
        main_layout.add_widget(notes_tab)
        main_layout.add_widget(apps_tab)
        
        # Load existing data
        self.load_tasks()
        self.load_notes()
        
        return main_layout
    
    def add_task(self, instance):
        title = self.task_input.text.strip()
        if title:
            task = {
                'id': len(self.data['tasks']) + 1,
                'title': title,
                'completed': False,
                'created_at': datetime.now().isoformat()
            }
            self.data['tasks'].append(task)
            self.save_data()
            self.task_input.text = ''
            self.load_tasks()
    
    def load_tasks(self):
        self.tasks_layout.clear_widgets()
        for task in self.data['tasks']:
            task_item = TaskItem(task, self.toggle_task, self.delete_task)
            self.tasks_layout.add_widget(task_item)
    
    def toggle_task(self, task_id):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                break
        self.save_data()
        self.load_tasks()
    
    def delete_task(self, task_id):
        self.data['tasks'] = [t for t in self.data['tasks'] if t['id'] != task_id]
        self.save_data()
        self.load_tasks()
    
    def add_note(self, instance):
        title = self.note_title.text.strip()
        content = self.note_content.text.strip()
        if title and content:
            note = {
                'id': len(self.data['notes']) + 1,
                'title': title,
                'content': content,
                'created_at': datetime.now().isoformat()
            }
            self.data['notes'].append(note)
            self.save_data()
            self.note_title.text = ''
            self.note_content.text = ''
            self.load_notes()
    
    def load_notes(self):
        self.notes_layout.clear_widgets()
        for note in self.data['notes']:
            note_item = NoteItem(note, self.delete_note)
            self.notes_layout.add_widget(note_item)
    
    def delete_note(self, note_id):
        self.data['notes'] = [n for n in self.data['notes'] if n['id'] != note_id]
        self.save_data()
        self.load_notes()
    
    def open_qacademico(self, instance):
        # Try to open in browser
        try:
            webbrowser.open('https://academico.iff.edu.br/qacademico/index.asp?t=1001')
        except:
            # Fallback: show popup with URL
            popup = Popup(
                title='Q-Acadêmico',
                content=Label(text='Acesse: https://academico.iff.edu.br/qacademico/index.asp?t=1001'),
                size_hint=(0.8, 0.4)
            )
            popup.open()

if __name__ == '__main__':
    UniversalApp().run() 