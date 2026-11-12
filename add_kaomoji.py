import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt

DICT_PATH = os.path.expanduser("~/.config/ibus/rime/kaomoji_custom.dict.yaml")
HEADER = """# Rime dictionary
# encoding: utf-8
---
name: kaomoji_custom
version: "1.0"
sort: by_weight
use_preset_vocabulary: false
...
"""

class KaomojiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_dict()
        self.initUI()

    def init_dict(self):
        if not os.path.exists(DICT_PATH):
            with open(DICT_PATH, 'w', encoding='utf-8') as f:
                f.write(HEADER)

    def initUI(self):
        self.setWindowTitle('Rime 颜文字管理器 (Qt版)')
        self.resize(500, 400)
        layout = QVBoxLayout()

        # --- 单条输入区 ---
        layout.addWidget(QLabel("<b>单条添加：</b>"))
        h_layout = QHBoxLayout()
        
        self.input_kaomoji = QLineEdit()
        self.input_kaomoji.setPlaceholderText("颜文字 (如 凸^-^凸)")
        self.input_trigger = QLineEdit()
        self.input_trigger.setPlaceholderText("触发词 (如 tu)")
        self.input_weight = QLineEdit()
        self.input_weight.setPlaceholderText("权重 (默认100)")
        
        h_layout.addWidget(self.input_kaomoji)
        h_layout.addWidget(self.input_trigger)
        h_layout.addWidget(self.input_weight)
        layout.addLayout(h_layout)

        btn_single = QPushButton("添加单条")
        btn_single.clicked.connect(self.add_single)
        layout.addWidget(btn_single)

        # --- 批量输入区 ---
        layout.addWidget(QLabel("<b>批量添加 (格式: 颜文字|触发词|权重)：</b>"))
        self.batch_text = QTextEdit()
        self.batch_text.setPlaceholderText("凸^-^凸|tu|100\nヽ(✿ﾟ▽ﾟ)ノ|kaixin|100")
        layout.addWidget(self.batch_text)

        btn_batch = QPushButton("批量导入")
        btn_batch.clicked.connect(self.add_batch)
        layout.addWidget(btn_batch)

        self.setLayout(layout)

    def clean_build(self):
        os.system("rm -rf ~/.config/ibus/rime/build/")

    def add_single(self):
        text = self.input_kaomoji.text().strip()
        trigger = self.input_trigger.text().strip()
        weight = self.input_weight.text().strip() or "100"
        
        if text and trigger:
            with open(DICT_PATH, 'a', encoding='utf-8') as f:
                f.write(f"{text}\t{trigger}\t{weight}\n")
            self.clean_build()
            QMessageBox.information(self, "成功", "添加成功！请右键 Rime 图标重新部署。")
            self.input_kaomoji.clear()
            self.input_trigger.clear()
        else:
            QMessageBox.warning(self, "错误", "颜文字和触发词不能为空！")

    def add_batch(self):
        content = self.batch_text.toPlainText().strip()
        if not content:
            return
        
        lines = content.split('\n')
        count = 0
        with open(DICT_PATH, 'a', encoding='utf-8') as f:
            for line in lines:
                parts = line.split('|')
                if len(parts) >= 2:
                    kaomoji = parts[0].strip()
                    trigger = parts[1].strip()
                    weight = parts[2].strip() if len(parts) > 2 else "100"
                    f.write(f"{kaomoji}\t{trigger}\t{weight}\n")
                    count += 1
        
        self.clean_build()
        QMessageBox.information(self, "成功", f"成功批量添加 {count} 条！请右键 Rime 图标重新部署。")
        self.batch_text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KaomojiApp()
    ex.show()
    sys.exit(app.exec())
