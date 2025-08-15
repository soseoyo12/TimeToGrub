import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import time
import mutagen
from voice_to_text import VoiceToText
from tkinterdnd2 import DND_FILES, TkinterDnD

class EnhancedVoiceToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("음성-텍스트 변환기 (Whisper)")
        self.root.geometry("850x700")
        self.root.minsize(600, 500)
        
        self.vtt = None
        self.selected_file = None
        self.audio_duration = 0
        self.start_time = 0
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # 제목
        title_label = ttk.Label(main_frame, text="음성 파일을 드래그하거나 선택하세요", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 설정 프레임
        settings_frame = ttk.LabelFrame(main_frame, text="변환 설정", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # 모델 선택
        ttk.Label(settings_frame, text="모델:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value="medium")
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, 
                                  values=["tiny", "base", "small", "medium", "large"],
                                  state="readonly", width=15)
        model_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        model_info = {
            "tiny": "가장 빠름 (39MB)",
            "base": "빠름 (74MB)", 
            "small": "보통 (244MB)",
            "medium": "정확함 (769MB) - 권장",
            "large": "가장 정확함 (1550MB)"
        }
        
        self.model_info_label = ttk.Label(settings_frame, 
                                         text=model_info[self.model_var.get()],
                                         font=("Arial", 9))
        self.model_info_label.grid(row=0, column=2, padx=(10, 0), pady=5)
        
        def on_model_change(event=None):
            self.model_info_label.config(text=model_info[self.model_var.get()])
        model_combo.bind('<<ComboboxSelected>>', on_model_change)
        
        # 언어 선택
        ttk.Label(settings_frame, text="언어:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value="ko")
        language_entry = ttk.Entry(settings_frame, textvariable=self.language_var, width=15)
        language_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(settings_frame, text="ko=한국어, en=영어, ja=일본어, auto=자동",
                 font=("Arial", 9)).grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # 드래그앤드롭 영역
        self.drop_frame = tk.Frame(main_frame, bg="#f0f0f0", relief="ridge", bd=2)
        self.drop_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                           pady=10, ipady=30)
        self.drop_frame.columnconfigure(0, weight=1)
        
        self.drop_label = tk.Label(self.drop_frame, 
                                 text="🎵 음성 파일을 여기에 드래그하세요\\n\\n지원 형식: MP3, WAV, M4A, MP4, FLAC, OGG",
                                 bg="#f0f0f0", font=("Arial", 12), fg="#666666")
        self.drop_label.pack(pady=20)
        
        # 드래그앤드롭 설정
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        # 파일 정보 표시
        self.file_info_frame = ttk.LabelFrame(main_frame, text="파일 정보", padding="5")
        self.file_info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                                 pady=(0, 10))
        self.file_info_frame.columnconfigure(1, weight=1)
        
        self.file_name_label = ttk.Label(self.file_info_frame, text="파일: 선택되지 않음")
        self.file_name_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.duration_label = ttk.Label(self.file_info_frame, text="")
        self.duration_label.grid(row=1, column=0, sticky=tk.W)
        
        self.estimated_time_label = ttk.Label(self.file_info_frame, text="")
        self.estimated_time_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        self.select_button = ttk.Button(button_frame, text="📁 파일 선택", 
                                      command=self.select_file)
        self.select_button.grid(row=0, column=0, padx=5)
        
        self.convert_button = ttk.Button(button_frame, text="🚀 변환 시작", 
                                       command=self.start_conversion, state="disabled")
        self.convert_button.grid(row=0, column=1, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="💾 결과 저장", 
                                    command=self.save_result, state="disabled")
        self.save_button.grid(row=0, column=2, padx=5)
        
        # 진행 상황 프레임
        progress_frame = ttk.LabelFrame(main_frame, text="진행 상황", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # 진행률 표시
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                       maximum=100, length=400)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 상태 정보 프레임
        status_info_frame = ttk.Frame(progress_frame)
        status_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        status_info_frame.columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(status_info_frame, text="파일을 선택하세요")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(status_info_frame, text="")
        self.time_label.grid(row=0, column=1, sticky=tk.E)
        
        # 결과 표시
        result_frame = ttk.LabelFrame(main_frame, text="변환 결과", padding="5")
        result_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(0, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=12, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.rowconfigure(6, weight=1)
        
    def get_audio_duration(self, file_path):
        try:
            audio = mutagen.File(file_path)
            if audio is not None:
                return audio.info.length
            return 0
        except:
            return 0
            
    def format_duration(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
        
    def estimate_conversion_time(self, duration, model_size):
        # 대략적인 변환 시간 추정 (실제 성능에 따라 다름)
        time_factors = {
            "tiny": 0.1,
            "base": 0.15,
            "small": 0.2,
            "medium": 0.3,
            "large": 0.5
        }
        return duration * time_factors.get(model_size, 0.3)
        
    def update_file_info(self, file_path):
        self.audio_duration = self.get_audio_duration(file_path)
        file_name = os.path.basename(file_path)
        
        self.file_name_label.config(text=f"파일: {file_name}")
        
        if self.audio_duration > 0:
            duration_text = f"재생 시간: {self.format_duration(self.audio_duration)}"
            self.duration_label.config(text=duration_text)
            
            estimated_time = self.estimate_conversion_time(self.audio_duration, self.model_var.get())
            est_text = f"예상 변환 시간: 약 {self.format_duration(estimated_time)}"
            self.estimated_time_label.config(text=est_text)
        else:
            self.duration_label.config(text="재생 시간: 알 수 없음")
            self.estimated_time_label.config(text="")
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            if self.is_audio_file(file_path):
                self.selected_file = file_path
                self.update_drop_area(f"✅ 선택됨: {os.path.basename(file_path)}")
                self.update_file_info(file_path)
                self.convert_button.config(state="normal")
                self.status_label.config(text="변환 준비 완료")
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
            self.update_drop_area(f"✅ 선택됨: {os.path.basename(file_path)}")
            self.update_file_info(file_path)
            self.convert_button.config(state="normal")
            self.status_label.config(text="변환 준비 완료")
            
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
        self.progress_var.set(0)
        self.start_time = time.time()
        self.status_label.config(text="변환 준비 중...")
        self.time_label.config(text="")
        self.result_text.delete(1.0, tk.END)
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self.convert_audio)
        thread.daemon = True
        thread.start()
        
        # 진행률 업데이트 시작
        self.update_progress()
        
    def update_progress(self):
        if self.convert_button['state'] == 'disabled':
            elapsed = time.time() - self.start_time
            if self.audio_duration > 0:
                estimated_total = self.estimate_conversion_time(self.audio_duration, self.model_var.get())
                progress_percent = min(95, (elapsed / estimated_total) * 100)
                self.progress_var.set(progress_percent)
            else:
                # 지속적인 진행률 애니메이션
                current = self.progress_var.get()
                if current >= 95:
                    self.progress_var.set(0)
                else:
                    self.progress_var.set(current + 1)
            
            # 경과 시간 표시
            self.time_label.config(text=f"경과 시간: {self.format_duration(elapsed)}")
            
            # 0.5초마다 업데이트
            self.root.after(500, self.update_progress)
        
    def convert_audio(self):
        try:
            if not self.vtt or getattr(self.vtt, '_current_model', None) != self.model_var.get():
                self.root.after(0, lambda: self.status_label.config(text="모델 로딩 중..."))
                self.vtt = VoiceToText(model_size=self.model_var.get())
                self.vtt._current_model = self.model_var.get()
            
            self.root.after(0, lambda: self.status_label.config(text="음성 변환 중..."))
            result = self.vtt.transcribe_audio(self.selected_file, language=self.language_var.get())
            
            self.root.after(0, lambda: self.conversion_complete(result))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.conversion_error(error_msg))
            
    def conversion_complete(self, result):
        self.progress_var.set(100)
        self.convert_button.config(state="normal")
        self.select_button.config(state="normal")
        self.save_button.config(state="normal")
        
        total_time = time.time() - self.start_time
        self.status_label.config(text="✅ 변환 완료!")
        self.time_label.config(text=f"총 소요 시간: {self.format_duration(total_time)}")
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result['text'])
        
        messagebox.showinfo("완료", f"음성 변환이 완료되었습니다!\\n소요 시간: {self.format_duration(total_time)}")
        
    def conversion_error(self, error_message):
        self.progress_var.set(0)
        self.convert_button.config(state="normal")
        self.select_button.config(state="normal")
        self.status_label.config(text="❌ 변환 실패")
        self.time_label.config(text="")
        
        messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\\n{error_message}")
        
    def save_result(self):
        if not self.result_text.get(1.0, tk.END).strip():
            messagebox.showwarning("경고", "저장할 결과가 없습니다.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="결과 저장",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"), 
                ("Word documents", "*.docx"),
                ("All files", "*.*")
            ]
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
    app = EnhancedVoiceToTextGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()