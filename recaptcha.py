import os
import urllib.request
import random
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pydub
import speech_recognition


class RecaptchaSolver:
    """A class to solve reCAPTCHA challenges using audio recognition."""

    # Constants
    TEMP_DIR = os.getenv("TEMP") if os.name == "nt" else "/tmp"
    TIMEOUT_STANDARD = 7
    TIMEOUT_SHORT = 5
    TIMEOUT_DETECTION = 0.05

    def __init__(self, driver: webdriver.Chrome) -> None:
        """Initialize the solver with a Selenium WebDriver instance.

        Args:
            driver: Selenium WebDriver instance for browser interaction
        """
        self.driver = driver
        self.action = ActionChains(self.driver)

    def solveCaptcha(self) -> None:
        """Attempt to solve the reCAPTCHA challenge.

        Raises:
            Exception: If captcha solving fails or bot is detected
        """
        # Wait for and switch to the reCAPTCHA iframe
        WebDriverWait(self.driver, self.TIMEOUT_STANDARD).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[@title='reCAPTCHA']")
            )
        )

        # Click the checkbox
        WebDriverWait(self.driver, self.TIMEOUT_STANDARD).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "rc-anchor-content"))
        ).click()

        # Check if solved by just clicking
        if self.is_solved():
            self.driver.switch_to.default_content()
            return

        # Switch back to the main content and locate the audio challenge iframe
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, self.TIMEOUT_STANDARD).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@title, 'recaptcha')]")
            )
        )

        # Click the audio challenge button
        WebDriverWait(self.driver, self.TIMEOUT_STANDARD).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
        ).click()
        time.sleep(0.3)

        if self.is_detected():
            raise Exception("Captcha detected bot behavior")

        # Wait for and process the audio challenge
        audio_source = WebDriverWait(self.driver, self.TIMEOUT_STANDARD).until(
            EC.presence_of_element_located((By.ID, "audio-source"))
        )
        audio_url = audio_source.get_attribute("src")

        try:
            text_response = self._process_audio_challenge(audio_url)
            response_box = self.driver.find_element(By.ID, "audio-response")
            response_box.send_keys(text_response.lower())
            self.driver.find_element(By.ID, "recaptcha-verify-button").click()
            time.sleep(0.4)

            # if not self.is_solved():
            #     raise Exception("Failed to solve the captcha")

        except Exception as e:
            raise Exception(f"Audio challenge failed: {str(e)}")

        finally:
            self.driver.switch_to.default_content()

    def _process_audio_challenge(self, audio_url: str) -> str:
        """Process the audio challenge and return the recognized text.

        Args:
            audio_url: URL of the audio file to process

        Returns:
            str: Recognized text from the audio file
        """
        mp3_path = os.path.join(self.TEMP_DIR, f"{random.randrange(1,1000)}.mp3")
        wav_path = os.path.join(self.TEMP_DIR, f"{random.randrange(1,1000)}.wav")

        try:
            urllib.request.urlretrieve(audio_url, mp3_path)
            sound = pydub.AudioSegment.from_mp3(mp3_path)
            sound.export(wav_path, format="wav")

            recognizer = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(wav_path) as source:
                audio = recognizer.record(source)

            return recognizer.recognize_google(audio)

        finally:
            for path in (mp3_path, wav_path):
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    def is_solved(self) -> bool:
        """Check if the captcha has been solved successfully."""
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, self.TIMEOUT_SHORT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "recaptcha-checkbox-checkmark")
                )
            )
            return True
        except Exception:
            return False

    def is_detected(self) -> bool:
        """Check if the bot has been detected."""
        try:
            self.driver.find_element(By.XPATH, "//*[text()='Try again later']")
            return True
        except Exception:
            return False

    def get_token(self) -> Optional[str]:
        """Get the reCAPTCHA token if available."""
        try:
            return self.driver.find_element(By.ID, "recaptcha-token").get_attribute(
                "value"
            )
        except Exception:
            return None
