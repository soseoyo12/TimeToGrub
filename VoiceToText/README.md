# Voice to Text with Whisper

OpenAI Whisper를 사용한 음성-텍스트 변환 프로그램

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 1. GUI 애플리케이션 (권장)
```bash
python enhanced_gui.py
```

**기능:**
- 드래그앤드롭으로 파일 선택
- 실시간 진행률 표시
- 예상 소요 시간 계산
- 파일 정보 표시 (재생 시간 등)
- 모델 크기별 정보 제공

### 2. 명령행에서 사용
```bash
python voice_to_text.py sample.wav
python voice_to_text.py sample.wav --timestamps
python voice_to_text.py sample.wav --output result.txt
python voice_to_text.py sample.wav --model medium --language ko
```

### 3. Python 코드에서 사용
```python
from voice_to_text import VoiceToText

vtt = VoiceToText(model_size="medium")
result = vtt.transcribe_audio("sample.wav", language="ko")
print(result['text'])
```

## 지원 파일 형식
- MP3, WAV, M4A, MP4, FLAC, OGG 등

## 모델 크기
- **tiny**: 가장 빠름 (39MB)
- **base**: 빠름 (74MB) 
- **small**: 보통 (244MB)
- **medium**: 정확함 (769MB) - 권장
- **large**: 가장 정확함 (1550MB)