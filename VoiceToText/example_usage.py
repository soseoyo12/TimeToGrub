from voice_to_text import VoiceToText

# 기본 사용법
def basic_example():
    vtt = VoiceToText(model_size="medium")
    
    # 음성 파일 경로 (mp3, wav, m4a 등 지원)
    audio_file = "sample.wav"
    
    try:
        result = vtt.transcribe_audio(audio_file, language="ko")
        print("변환된 텍스트:")
        print(result['text'])
        print(f"감지된 언어: {result['language']}")
    except FileNotFoundError:
        print("음성 파일을 찾을 수 없습니다.")

# 타임스탬프 포함 변환
def timestamp_example():
    vtt = VoiceToText(model_size="medium")
    audio_file = "sample.wav"
    
    try:
        result = vtt.transcribe_with_timestamps(audio_file, language="ko")
        print("타임스탬프가 포함된 변환 결과:")
        print(result)
    except FileNotFoundError:
        print("음성 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    print("=== 기본 예제 ===")
    basic_example()
    print("\n=== 타임스탬프 예제 ===")
    timestamp_example()