import os
import string
import subprocess
import numpy as np

from scipy.io.wavfile import read, write


def abs_path(path):
    return os.path.abspath(path)


def join_paths(*paths):
    return os.path.join(*paths)


def sndread_dir(dir_path):
    abs_dir_path = abs_path(dir_path)

    return [
        sndread(join_paths(abs_dir_path, path))
        for path in os.listdir(abs_dir_path)
    ]


def sndread(path):
    sample_rate, signal = read(abs_path(path))
    signal = signal.astype(float) / np.abs(signal).max()

    return sample_rate, signal


def play(data, fs=44100):
    write('./data/output.wav', fs, data)
    subprocess.call(["afplay", './data/output.wav'])


def load_corpus(path):
    abs_file_path = abs_path(path)

    with open(abs_file_path) as fs:
        no_punctuation = str.maketrans('', '', string.punctuation)
        corpus = fs.read().lower().translate(no_punctuation).split()

    return corpus


def make_vocab(corpus):
    word_to_id = {}
    id_to_word = {}

    identity = 0

    for word in corpus:
        if word not in word_to_id:
            word_to_id[word] = identity
            id_to_word[identity] = word
            identity += 1

    return word_to_id, id_to_word