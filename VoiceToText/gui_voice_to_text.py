import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from voice_to_text import VoiceToText
from tkinterdnd2 import DND_FILES, TkinterDnD

class VoiceToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("음성-텍스트 변환기 (Whisper)")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        self.vtt = None
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 제목
        title_label = ttk.Label(main_frame, text="음성 파일을 드래그하거나 선택하세요", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 모델 선택
        ttk.Label(main_frame, text="모델:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value="medium")
        model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, 
                                  values=["tiny", "base", "small", "medium", "large"],
                                  state="readonly", width=15)
        model_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 언어 선택
        ttk.Label(main_frame, text="언어:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value="ko")
        language_entry = ttk.Entry(main_frame, textvariable=self.language_var, width=15)
        language_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 드래그앤드롭 영역
        self.drop_frame = tk.Frame(main_frame, bg="lightgray", relief="ridge", bd=2)
        self.drop_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                           pady=10)
        self.drop_frame.columnconfigure(0, weight=1)
        self.drop_frame.rowconfigure(0, weight=1)
        
        self.drop_label = tk.Label(self.drop_frame, 
                                 text="음성 파일을 여기에 드래그하세요\\n\\n지원 형식: MP3, WAV, M4A, MP4, FLAC",
                                 bg="lightgray", font=("Arial", 12))
        self.drop_label.grid(row=0, column=0, pady=50)
        
        # 드래그앤드롭 설정
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        # 파일 선택 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.select_button = ttk.Button(button_frame, text="파일 선택", 
                                      command=self.select_file)
        self.select_button.grid(row=0, column=0, padx=5)
        
        self.convert_button = ttk.Button(button_frame, text="변환 시작", 
                                       command=self.start_conversion, state="disabled")
        self.convert_button.grid(row=0, column=1, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="결과 저장", 
                                    command=self.save_result, state="disabled")
        self.save_button.grid(row=0, column=2, padx=5)
        
        # 진행 상황
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(main_frame, text="파일을 선택하세요")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # 결과 표시
        result_frame = ttk.LabelFrame(main_frame, text="변환 결과", padding="5")
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.rowconfigure(7, weight=1)
        
        self.selected_file = None
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            if self.is_audio_file(file_path):
                self.selected_file = file_path
                self.update_drop_area(f"선택된 파일: {os.path.basename(file_path)}")
                self.convert_button.config(state="normal")
                self.status_label.config(text=f"파일 선택됨: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("오류", "지원하지 않는 파일 형식입니다.")
                
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="음성 파일 선택",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.m4a *.mp4 *.flac *.ogg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            self.update_drop_area(f"선택된 파일: {os.path.basename(file_path)}")
            self.convert_button.config(state="normal")
            self.status_label.config(text=f"파일 선택됨: {os.path.basename(file_path)}")
            
    def update_drop_area(self, text):
        self.drop_label.config(text=text)
        
    def is_audio_file(self, file_path):
        audio_extensions = {'.mp3', '.wav', '.m4a', '.mp4', '.flac', '.ogg', '.aac'}
        return os.path.splitext(file_path.lower())[1] in audio_extensions
        
    def start_conversion(self):
        if not self.selected_file:
            messagebox.showerror("오류", "먼저 파일을 선택하세요.")
            return
            
        self.convert_button.config(state="disabled")
        self.select_button.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="변환 중...")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self.convert_audio)
        thread.daemon = True
        thread.start()
        
    def convert_audio(self):
        try:
            if not self.vtt or self.vtt.model.device != self.model_var.get():
                self.root.after(0, lambda: self.status_label.config(text="모델 로딩 중..."))
                self.vtt = VoiceToText(model_size=self.model_var.get())
            
            self.root.after(0, lambda: self.status_label.config(text="음성 변환 중..."))
            result = self.vtt.transcribe_audio(self.selected_file, language=self.language_var.get())
            
            self.root.after(0, lambda: self.conversion_complete(result))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.conversion_error(error_msg))
            
    def conversion_complete(self, result):
        self.progress.stop()
        self.convert_button.config(state="normal")
        self.select_button.config(state="normal")
        self.save_button.config(state="normal")
        self.status_label.config(text="변환 완료!")
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result['text'])
        
        messagebox.showinfo("완료", "음성 변환이 완료되었습니다!")
        
    def conversion_error(self, error_message):
        self.progress.stop()
        self.convert_button.config(state="normal")
        self.select_button.config(state="normal")
        self.status_label.config(text="변환 실패")
        
        messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\\n{error_message}")
        
    def save_result(self):
        if not self.result_text.get(1.0, tk.END).strip():
            messagebox.showwarning("경고", "저장할 결과가 없습니다.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="결과 저장",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.result_text.get(1.0, tk.END))
                messagebox.showinfo("저장 완료", f"결과가 저장되었습니다:\\n{file_path}")
            except Exception as e:
                messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다:\\n{e}")

def main():
    root = TkinterDnD.Tk()
    app = VoiceToTextGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()