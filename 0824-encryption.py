import copy
import json
import random

import matplotlib.pyplot as plt
from collections import Counter


class simple_shift_encryption:
    def __init__(self):
        self.test()

    def load_shakspeara_novel(self, path="source/shakspeara.txt"):
        with open(path, "r") as f:
            novelcontent = f.read()
        return novelcontent

    def frequency_of_string(self, text):
        content = dict(Counter(text))
        alpha = sorted(content, key=lambda x: content[x], reverse=True)
        return alpha, [content[i] for i in alpha]

    def simple_adding_encrypt(self, text):
        letters = set(list(text))
        values = [i for i in map(ord, letters)]
        keys = copy.deepcopy(values)
        random.shuffle(keys)
        encrypt_dict = dict([(keys[i], values[i]) for i in range(len(values))])
        return "".join([chr(encrypt_dict[ord(s)]) for s in list(text)]), encrypt_dict

    def test(self, ):
        plot_path = {
            "original": "plot/shakspeara_novel_original_letter_frequency.png",
            "encrypted": "plot/shakspeara_novel_encrypted_letter_frequency.png",
        }
        novel = self.load_shakspeara_novel()
        letters, novel_letter_frequency = self.frequency_of_string(novel)
        print(letters, novel_letter_frequency)
        plt.bar(letters, novel_letter_frequency, width=0.9)
        plt.savefig(plot_path["original"], dpi=90)
        plt.show()
        encryp_text, encryp_dict = self.simple_adding_encrypt(novel)
        encryp_letter, encryp_letter_freq = self.frequency_of_string(encryp_text)
        print(encryp_letter, encryp_letter_freq)
        plt.bar(encryp_letter, encryp_letter_freq, width=0.9)
        plt.savefig(plot_path["encrypted"], dpi=90)
        plt.show()
        shakspeara_encryption = {
            "originalText": novel,
            "encryptedText": encryp_text,
            "encryptedDict": encryp_dict,
            "Addition": {
                "originalText":
                    {
                        "letters": letters,
                        "frequency": novel_letter_frequency,
                        "fig": plot_path["original"],
                    },
                "encryptedText":
                    {
                        "letters": encryp_letter,
                        "frequency": encryp_letter_freq,
                        "fig": plot_path["encrypted"],
                    },
                "plotPath": plot_path,
            }
        }
        json.dump(shakspeara_encryption, open("source/shakspeara_encryption_info.json", "w+"))
        return shakspeara_encryption


class muchComplexEncryption:
    def __init__(self):
        pass


if __name__ == "__main__":
    simple_shift_encryption()
