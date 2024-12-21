import time
from pathlib import Path
import pdfplumber
from converter import convert_to_pdf
import os
import pyttsx3
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment


def save_audio(page_text, file_path, page_number, audio_dir):
    """Сохраняет аудио для одной страницы"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Установите скорость речи

    output_file = Path(file_path).stem + f"_{page_number}.mp3"
    output_path = os.path.join(audio_dir, output_file)

    engine.save_to_file(page_text, output_path)
    engine.runAndWait()

    return output_path


def merge_audio(files, output_file):
    audio_segments = [AudioSegment.from_wav(file) for file in files]

    combined_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        combined_audio += segment

    combined_audio.export(output_file, format="wav")
    print(f"Файл объединен в {output_file}")
    return output_file

def pdf_to_mp3(file_path: str, language: str, AUDIO_DIR: str):
    if not os.path.exists(AUDIO_DIR):
        os.mkdir(AUDIO_DIR)

    if Path(file_path).suffix != '.pdf':
        print("Конвертирую файл")
        file_path = convert_to_pdf(file_path)

    if Path(file_path).is_file():
        with pdfplumber.PDF.open(file_path) as pdf:
            num_of_pages = len(pdf.pages)
            pages = [page.extract_text() for page in pdf.pages]

        print(f"Обрабатываю {num_of_pages} страниц...")

        audio_files = []
        start_time = time.time()

        with ThreadPoolExecutor() as executor:
            futures = []
            for i, page_text in enumerate(pages, start=1):
                if i == 1:
                    text_lines = page_text.splitlines()
                    text_lines = text_lines[2:]
                    page_text = '\n'.join(text_lines)
                future = executor.submit(save_audio, page_text, file_path, i, AUDIO_DIR)

                futures.append(future)

            for future in futures:
                audio_files.append(future.result())

        file_name = Path(file_path).stem
        output_file = os.path.join(AUDIO_DIR, f"{file_name}.mp3")
        merge_audio(audio_files, output_file)

        end_time = time.time()

        print(f"Время обработки: {end_time - start_time} секунд")
        return f"{file_name}.mp3"
    else:
        return None
