Бот - https://t.me/TableReader_bot. Для его работы должен быть запущен либо у меня, либо локально (но там нужно установить одну программу)
Функционал обработки pdf повторяет предыдущее задание
Для обработки jpg файлов на машине должен быть установлен Tesseract (https://github.com/UB-Mannheim/tesseract/wiki) для распознавания таблиц
и дополнительно rus.traindata для обработки ФИО (https://github.com/tesseract-ocr/tessdata/blob/main/rus.traineddata)

Обработка jpg файла не гарантирует 100%. В частности в примерной таблице часть ФИО обрезана из-за чего распознаются не полностью.

Прикладываю скрины с результатом работы.
![image](https://github.com/user-attachments/assets/9424c40a-c49e-423e-be72-c00be29d2e86)

![image](https://github.com/user-attachments/assets/06ab153a-7487-40d6-8617-5bf99922de68)

