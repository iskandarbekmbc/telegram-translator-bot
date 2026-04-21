import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

BOT_TOKEN = "8574528463:AAFVA0xL89fSVGeD5YYSDSqFS8obSxruvEw"


def is_english(text: str) -> bool:
    """
    Tilni aniqlash: 'en' chiqsa inglizcha deb hisoblaymiz.
    Qisqa matnlarda xato bo'lishi mumkin.
    """
    try:
        lang = detect(text)
        return lang == "en"
    except LangDetectException:
        return False


def translate_auto(text: str) -> tuple[str, str]:
    """
    Matn inglizcha bo'lsa EN->UZ, bo'lmasa UZ->EN.
    Natija: (label, translated_text)
    """
    text = text.strip()
    if not text:
        return ("", "")

    if is_english(text):
        result = GoogleTranslator(source="en", target="uz").translate(text)
        return ("EN -> UZ", result)
    else:
        result = GoogleTranslator(source="uz", target="en").translate(text)
        return ("UZ -> EN", result)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start(message: Message):
        await message.answer(
            "Assalomu alaykum! Men avtomatik tarjimon botman.\n"
            "Matn yuboring, o'zim EN yoki UZ ekanini aniqlab, teskarisiga tarjima qilaman."
        )

    @dp.message(Command("help"))
    async def help_cmd(message: Message):
        await message.answer(
            "Qanday ishlaydi:\n"
            "- Inglizcha matn yuborsangiz -> o'zbekchaga tarjima qiladi\n"
            "- O'zbekcha matn yuborsangiz -> inglizchaga tarjima qiladi\n\n"
            "Eslatma: juda qisqa matnlarda (masalan, 'ok', 'hi') tilni xato topishi mumkin."
        )

    @dp.message(F.text)
    async def handle_text(message: Message):
        try:
            label, translated = translate_auto(message.text)
        except Exception:
            await message.answer(
                "Tarjima vaqtida xatolik bo'ldi. Birozdan keyin qayta urinib ko'ring.\n"
                "Agar tez-tez takrorlansa, boshqa bepul usulga o'tkazamiz."
            )
            return

        if not translated:
            await message.answer("Matn bo'sh ko'rinyapti. Iltimos matn yuboring.")
            return

        await message.answer("(" + label + ")\n" + translated)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
