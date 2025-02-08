#!/usr/bin/env python3

import cv2
import pytesseract
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def translate_text(text, target_lang="es", source_lang="auto"):

    url = "https://libretranslate.com/translate"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text",
        "alternatives": 100, 
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            result = response.json()
            return result.get("translatedText", "")
        else:
            print("Translation error: HTTP", response.status_code)
            return ""
    except Exception as e:
        print("Translation exception:", e)
        return ""

def main():
    # Change '0' to the correct video source index or a video file path.
    video_source = 'test.mp4'  # Use 0 for the default webcam, or change to 'your_video.mp4' for a video file
    
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source '{video_source}'.")
        return

    # Set your desired target language code (e.g., 'es' for Spanish, 'fr' for French).
    target_language = 'English'
    print("Starting video processing. Press 'Esc' to exit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video or unable to fetch the frame.")
            break

        # Convert the frame to grayscale for better OCR performance.
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use Tesseract OCR to extract text from the grayscale image.
        detected_text = pytesseract.image_to_string(gray_frame)

        if detected_text.strip():
            print("Detected text:")
            print(detected_text)
            
            # Translate the detected text using the updated LibreTranslate API call.
            translated_text = translate_text(detected_text, target_lang=target_language)
            print("Translated text:")
            print(translated_text)
            
            # Overlay the translated text onto the frame.
            if translated_text:
                cv2.putText(
                    frame,
                    translated_text,
                    (10, 50),                     # Position: x, y coordinates
                    cv2.FONT_HERSHEY_SIMPLEX,      # Font type
                    1,                           # Font scale
                    (0, 255, 0),                 # Color (green in BGR)
                    2,                           # Thickness
                    cv2.LINE_AA                  # Line type (anti-aliased)
                )

        # Display the frame with the overlay.
        cv2.imshow("Translated Video", frame)

        # Wait for 1 millisecond and check if the user pressed the 'Esc' key (ASCII code 27) to exit.
        if cv2.waitKey(1) & 0xFF == 27:
            print("Exiting video processing.")
            break

    # Release the video capture and close windows.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

