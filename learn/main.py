import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, regularizers, models, callbacks
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import pickle
import random
from nltk.corpus import wordnet
import nltk
#загружаем словарь для синонимизации данных(txt которые находятся в папке data для обучения нйросети)
nltk.download('wordnet')

# Функции аугментации(это когда из сущ. данных делаются новые. Перестановка слов и тд)
def swap_words(text, n=2):
    words = text.split()
    if len(words) < 2:
        return text
    for _ in range(n):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]
    return ' '.join(words)

#фунекция синонимизвции
def replace_synonyms(text, n=1):
    words = text.split()
    for _ in range(n):
        idx = random.randint(0, len(words) - 1)
        synonyms = wordnet.synsets(words[idx])
        if synonyms:
            lemmas = [lemma.name().replace('_', ' ') for lemma in synonyms[0].lemmas()]
            if lemmas:
                words[idx] = random.choice(lemmas)
    return ' '.join(words)

# Параметры модели
embedding_dim = 300 #сколько "смысла" имеет каждое слово
padding_type = 'post'
oov_tok = "<OOV>"#тип токинизации
num_epochs = 15 #кол-во эпох
batch_size = 70
learning_rate = 0.0003#балансировака веса
input_dim = 13000#каждое слово зание опрделенное место из 13000 
max_length = 80 #максимальная длинна в токенах

# Пути
positive_dir = 'learn/data/positive'
negative_dir = 'learn/data/negative'
neutral_dir = 'learn/data/neutral'
model_path = 'learn/model/my_model.keras'
tokenizer_path = 'learn/model/tokenizer.pkl'
hash_file = 'learn/model/data_count.txt'

# Создание директорий
os.makedirs(os.path.dirname(model_path), exist_ok=True)
os.makedirs(os.path.dirname(tokenizer_path), exist_ok=True)

# Функция подсчета файлов
def count_files(directories):
    return {directory: len(os.listdir(directory)) if os.path.exists(directory) else 0 for directory in directories}

# Функция загрузки данных с аугментацией
def load_data(directory):
    texts = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read().strip().lower()
                texts.append(text)
                texts.append(swap_words(text))  # Перестановка слов
                texts.append(replace_synonyms(text))  # Синонимизация
    return texts

# Проверка изменения количества файлов
new_file_counts = count_files([positive_dir, negative_dir, neutral_dir])
if os.path.exists(hash_file):
    with open(hash_file, 'r') as f:
        old_file_counts = {line.split(": ")[0]: int(line.split(": ")[1]) for line in f}
else:
    old_file_counts = {}

if new_file_counts != old_file_counts or not os.path.exists(model_path) or not os.path.exists(tokenizer_path):
    print("Количество файлов изменилось или модель не найдена. Обучаем новую модель.")
    
    # Загружаем данные
    positive_texts = load_data(positive_dir)
    negative_texts = load_data(negative_dir)
    neutral_texts = load_data(neutral_dir)
    
    if not (positive_texts or negative_texts or neutral_texts):
        raise ValueError("Ошибка: отсутствуют данные для обучения")
    
    texts = positive_texts + negative_texts + neutral_texts
    labels = ([1] * len(positive_texts) + [0] * len(negative_texts) + [2] * len(neutral_texts))
    
    tokenizer = Tokenizer(num_words=input_dim, oov_token=oov_tok)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences,maxlen=max_length, padding=padding_type)
    labels = np.array(labels)
    
    #Архитектура модели
    model = models.Sequential([
        layers.Embedding(input_dim=input_dim, output_dim=embedding_dim),
        layers.Bidirectional(layers.LSTM(64, return_sequences=True, dropout=0.2, kernel_regularizer=regularizers.l2(0.001))),#Обучение нейросети 1 слой(LSTM) 64 нйерогна, l2 это веса
        layers.Bidirectional(layers.LSTM(32, dropout=0.3, kernel_regularizer=regularizers.l2(0.02))),#Обучение нейросети 2 слой(LSTM) 32 нейрона, dropaout это случайное отключение нейронов
        layers.BatchNormalization(), 
        layers.Dropout(0.4),#случайное отключение 40% нейронов
        layers.Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        layers.Dropout(0.2),#Случайное отключение 20% нейронов
        layers.Dense(3, activation='softmax')#В итоге 3 класа (положительный, нейтральный и негативый)
    ])

    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), 
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    history = model.fit(padded, labels, epochs=num_epochs, batch_size=batch_size, 
                        validation_split=0.2, verbose=2, callbacks=[early_stopping, reduce_lr])#авто отключение если модель переобучается
    
    model.save(model_path)#сохраняем обученую модель

    with open(tokenizer_path, "wb") as f:
        pickle.dump(tokenizer, f)
    with open(hash_file, 'w') as f:
        for dir_path, count in new_file_counts.items():
            f.write(f"{dir_path}: {count}\n")
else:
    print("Количество файлов не изменилось. Загружаем существующую модель.")
    model = tf.keras.models.load_model(model_path)
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)

# Функция классификации
class_names = ["Отрицательный", "Положительный", "Нейтральный"]#3 возможных класса
def classify_text(text):
    if not text.strip(): #если пустой текст, то ошибка
        return "Ошибка: введен пустой текст"
    sequence = tokenizer.texts_to_sequences([text.lower().strip()])
    if not sequence or not sequence[0]:
        return "Классификация текста: Нейтральный (уверенность: 0.00)"
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding=padding_type)
    prediction = model.predict(padded_sequence)[0]
    class_index = np.argmax(prediction)
    return f"Классификация текста: {class_names[class_index]} (уверенность: {prediction[class_index]:.2f})"
