from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.animation import Animation
from kivy.clock import Clock
from brain import get_ai_response
import threading

Window.softinput_mode = "below_target"

KV = '''
MDScreen:
    md_bg_color: [0, 0, 0, 1]

    MDRaisedButton:
        text: "TERMINATE"
        pos_hint: {"center_x": 0.5, "center_y": 0.96}
        md_bg_color: [0.8, 0, 0, 1]
        on_release: app.stop_system()

    AsyncImage:
        id: ai_face
        source: 'https://img.freepik.com/free-photo/view-robot-human-hybrid_23-2151120033.jpg'
        size_hint: (0.45, 0.45)
        pos_hint: {"center_x": 0.5, "center_y": 0.78}

    MDLabel:
        text: "CHAT H - AGI"
        halign: "center"
        pos_hint: {"center_y": 0.62}
        font_style: "H5"
        theme_text_color: "Custom"
        text_color: [0, 0.8, 1, 1]

    ScrollView:
        pos_hint: {"center_x": 0.5, "center_y": 0.35}
        size_hint: (0.95, 0.45)
        do_scroll_x: False
        MDLabel:
            id: chat_logs
            text: ""
            markup: True
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            size_hint_y: None
            height: self.texture_size[1]
            halign: "left"
            valign: "top"
            padding: [20, 20]

    MDBoxLayout:
        orientation: "horizontal"
        size_hint: (1, 0.1)
        padding: "10dp"
        spacing: "10dp"
        pos_hint: {"center_y": 0.08}

        MDTextField:
            id: user_input
            hint_text: "Neural Link..."
            mode: "fill"
            fill_color_normal: [0.05, 0.05, 0.1, 1]
            size_hint_x: 0.8

        MDIconButton:
            icon: "send-circle"
            theme_text_color: "Custom"
            text_color: [0, 0.8, 1, 1]
            on_release: app.process_chat()
'''

class ChatHApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(lambda x: self.init_system(), 1)

    def init_system(self):
        self.root.ids.chat_logs.text = "[b][color=00FF00]>>> SYSTEM READY[/color][/b]"

    def animate_face(self):
        face = self.root.ids.ai_face
        anim = Animation(size_hint=(0.48, 0.48), duration=0.3) + Animation(size_hint=(0.45, 0.45), duration=0.3)
        anim.repeat = True
        anim.start(face)
        return anim

    def process_chat(self, *args):
        query = self.root.ids.user_input.text
        if query:
            self.root.ids.chat_logs.text += f"\\n\\n[b][color=FFFF00]User:[/color][/b]\\n{query}"
            threading.Thread(target=self.run_ai, args=(query,)).start()
            self.root.ids.user_input.text = ""

    def run_ai(self, query):
        face_anim = self.animate_face()
        try:
            response = get_ai_response(query)
            self.root.ids.chat_logs.text += f"\\n\\n[b][color=00BFFF]Chat H:[/color][/b]\\n{response}"
        except Exception as e:
            self.root.ids.chat_logs.text += f"\\n\\n[b][color=FF0000]Error:[/color][/b]\\n{str(e)}"
        
        face_anim.stop(self.root.ids.ai_face)

    def stop_system(self):
        self.stop()

if __name__ == "__main__":
    ChatHApp().run()
