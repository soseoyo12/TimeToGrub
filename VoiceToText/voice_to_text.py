import whisper
import os
import argparse

class VoiceToText:
    def __init__(self, model_size="medium"):
        """
        Whisper 모델 초기화
        model_size: tiny, base, small, medium, large
        """
        print(f"Whisper {model_size} 모델 로딩 중...")
        self.model = whisper.load_model(model_size)
        print("모델 로딩 완료!")
    
    def transcribe_audio(self, audio_file_path, language="ko"):
        """
        음성 파일을 텍스트로 변환
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {audio_file_path}")
        
        print(f"음성 파일 변환 중: {audio_file_path}")
        result = self.model.transcribe(
            audio_file_path, 
            language=language,
            fp16=False
        )
        
        return {
            'text': result["text"],
            'language': result.get("language", "unknown"),
            'segments': result.get("segments", [])
        }
    
    def transcribe_with_timestamps(self, audio_file_path, language="ko"):
        """
        타임스탬프와 함께 음성 파일을 텍스트로 변환
        """
        result = self.transcribe_audio(audio_file_path, language)
        
        formatted_output = []
        for segment in result['segments']:
            start_time = self.format_timestamp(segment['start'])
            end_time = self.format_timestamp(segment['end'])
            text = segment['text'].strip()
            formatted_output.append(f"[{start_time} -> {end_time}] {text}")
        
        return '\n'.join(formatted_output)
    
    def format_timestamp(self, seconds):
        """
        초를 mm:ss 형식으로 변환
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

def main():
    parser = argparse.ArgumentParser(description='Whisper를 사용한 음성-텍스트 변환')
    parser.add_argument('audio_file', help='변환할 음성 파일 경로')
    parser.add_argument('--model', default='medium', choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='사용할 Whisper 모델 크기 (기본값: medium)')
    parser.add_argument('--language', default='ko', help='음성 언어 (기본값: ko)')
    parser.add_argument('--timestamps', action='store_true', help='타임스탬프 포함')
    parser.add_argument('--output', help='출력 파일 경로 (옵션)')
    
    args = parser.parse_args()
    
    try:
        vtt = VoiceToText(args.model)
        
        if args.timestamps:
            result = vtt.transcribe_with_timestamps(args.audio_file, args.language)
        else:
            result = vtt.transcribe_audio(args.audio_file, args.language)['text']
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"결과가 {args.output}에 저장되었습니다.")
        else:
            print("\n=== 변환 결과 ===")
            print(result)
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()