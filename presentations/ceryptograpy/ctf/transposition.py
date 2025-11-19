from is_english import is_english_message
from itertools import permutations
import time

def string_to_array(input_string, num_rows, num_columns):
    matrix = [[' ' for _ in range(num_columns)] for _ in range(num_rows)]

    index = 0
    for row in range(num_rows):
        for col in range(num_columns):
            if index < len(input_string):
                matrix[row][col] = input_string[index]
                index += 1
    return matrix


def array_string_transposition(in_array, in_secret=None):
    new_message = ""
    index = 0
    cols = len(in_array[0])
    rows = len(in_array)
    actual_cols_list = range(cols)
    if in_secret is not None:
        actual_cols_list = in_secret
    for col in range(cols):
        for row in range(rows):
            if index < rows * cols:
                secret_col = list(actual_cols_list).index(col)
                new_message += in_array[row][secret_col]
                index += 1
    return new_message


def encrypt_transposition(message, in_key):
    cols = in_key
    # calculate the number of matrix rows
    rows = len(message) // in_key + 1 if len(message) % in_key != 0 else len(message) // in_key
    # make the message at (cols X rows) size
    message = message.ljust(cols * rows, " ")
    # create two dimensions array. Inserting the message line by line
    matrix = string_to_array(message, rows, cols)
    # create the cipher text by aggregating letters vertically for the array
    cipher_text = array_string_transposition(matrix)

    return cipher_text


def decrypt_transposition(cipher_text, in_key):
    cols = in_key
    rows = len(cipher_text) // in_key
    if len(cipher_text) % in_key != 0:
        rows = len(cipher_text) // in_key + 1
    original_text = ""

    for row in range(rows):
        for col in range(cols):
            pos = col * rows + row
            if pos < len(cipher_text):
                original_text += cipher_text[pos]

    return original_text


def encrypt_transposition_with_secret(message, in_key, in_secret=None):
    rows = len(message) // in_key
    cols = in_key

    if len(message) % in_key != 0:
        rows = len(message) // in_key + 1

    message = message.ljust(cols * rows, " ")
    matrix = string_to_array(message, rows, cols)
    if isinstance(in_secret, int) or isinstance(in_secret, str):
        in_secret = [int(digit)-1 for digit in str(in_secret)]
    cipher_text = array_string_transposition(matrix, in_secret)

    return cipher_text


def decrypt_transposition_with_secret(cipher_text, in_key, in_secret=None):
    # cols = in_key
    rows = len(cipher_text) // in_key
    if len(cipher_text) % in_key != 0:
        rows = len(cipher_text) // in_key + 1
    original_text = ""

    my_range = range(in_key)
    if in_secret is not None:
        if isinstance(in_secret, int) or isinstance(in_secret, str):
            my_range = [int(digit) - 1 for digit in str(in_secret)]

    for row in range(rows):
        for col in my_range:
            pos = col * rows + row
            if pos < len(cipher_text):
                original_text += cipher_text[pos]

    return original_text


def hacking_transposition(message):
    ret_value = None
    print('brute-force hacking transposition...')
    start = time.time()
    # brute-force by looping through every possible key
    for key in range(1, len(message)):
        print(f'Trying key #{key}...')
        decryptedText = decrypt_transposition(message, key)
        decryptedText = decryptedText.strip(' ')
        if is_english_message(decryptedText):
            print("=" * 100)
            print(f'Key {key}: {decryptedText[:100]}...')
            print()
            ret_value = decryptedText
            break
    end = time.time()
    duration = end - start
    print(f"Hack duration is {duration} seconds")
    return ret_value


def get_secrets_permutations(key):
    """
    Prepare list of string secrets for key of transposition cipher
    secret is a combination of numbers from 1 to key in different order
    :param key: number that represent number of columns in transposition cipher
    :return: list of all possible secrets for specific transposition key
    """
    my_list = list(range(1, key+1))
    # Generate all permutations
    all_permutations = list(permutations(my_list))
    secrets = []
    for permutation in all_permutations:
        secrets.append("".join(str(num) for num in permutation))
    return secrets


def hacking_transposition_with_secret(message):
    print('brute-force hacking transposition with secret...')
    ret_value = None
    start = time.time()
    # brute-force by looping through every possible key
    for key in range(1, len(message)):
        secrets = get_secrets_permutations(key)
        for secret in secrets:
            print(f'Trying key #{key}, secret #{secret}...')
            decryptedText = decrypt_transposition_with_secret(message, key, secret)
            decryptedText = decryptedText.strip(' ')
            if is_english_message(decryptedText):
                print("="*100)
                print(f'Key {key}, secret {secret}: {decryptedText[:100]}{"..." if len(decryptedText) > 100 else ""}')
                print()
                ret_value = decryptedText
                break
        if ret_value is not None:
            break
    end = time.time()
    duration = end - start
    print(f"Hack duration is {duration} seconds")

    return ret_value

if __name__ == "__main__":
    # Example usage
    # plaintext = "common sense is not so common."
    # plaintext = 'Three can keep a secret #$%fdr#@, if two of them are dead.'
    # plaintext = "I need to buy some groceries: an apple, orange, and banana. Don't forget to bring your umbrella " \
    #             "when it rains! The total cost is $15. Please be quiet (no loud talking). The function should return " \
    #             "the result {value}. Access the element in the list using square brackets [index]. Connect the red " \
    #             "wire to the positive terminal and the black wire to the negative terminal. Subtract 5 from the total " \
    #             "to get the final amount - $5. The temperature is expected to rise by 10 degrees. Add the numbers" \
    #             " 3 and 7 to get the sum + 10."
    # plaintext = """
    # I need to buy some groceries: an apple, orange, and banana. Don't forget to bring your umbrella
    # when it rains! The total cost is $15. Please be quiet (no loud talking). The function should return
    # the result {value}. Access the element in the list using square brackets [index]. Connect the red
    # wire to the positive terminal and the black wire to the negative terminal. Subtract 5 from the total
    # to get the final amount - $5. The temperature is expected to rise by 10 degrees. Add the numbers
    # 3 and 7 to get the sum + 10.
    # """
    # key = 11
    # plaintext = "A strong algorithm can solve any challenge; a strong mindset can solve any obstacle."
    # # Encryption
    # encrypted_text = encrypt_transposition(plaintext, key)
    # print("Encrypted:", encrypted_text)
    # # key = 5
    # # Decryption
    # decrypted_text = decrypt_transposition(encrypted_text, key)
    # print("Decrypted:", decrypted_text)
    # # secret = "32841756"
    # hacking_transposition(encrypted_text)
    # print("="*50)
    # key = 4
    # secret = 1432
    # a = encrypt_transposition_with_secret(plaintext, key, secret)
    # print(f"Encrypt text with secret [{secret}], key={key}:\n", a)
    # b = decrypt_transposition_with_secret(a, key, secret)
    # print(f"Decrypt text with secret [{secret}], key={key}:\n", b)
    #
    # hacking_transposition_with_secret(a)


    # secret = "53124"
    # a = encrypt_transposition_with_secret(plaintext, 5, secret)
    # # print(a)
    # b = decrypt_transposition_with_secret(a, 5, secret)
    # print(b)
    # plaintext = plaintext+ "  "
    # result_matrix = string_to_array(plaintext+ "  ", 4, 8)
    # print("[", end="")
    # index = 0
    # for row in range(4):
    #     print("[", end="")
    #     for col in range(8):
    #         print(f"'{plaintext[index]}'", end=", ")
    #         index += 1
    #     print("\b\b]")
    # print("]")

    text1 = "detective found four clues"
    text2 = "leading to building twenty two were"
    text3 = "the treasure was buried six feet under ground"


    enc1 = encrypt_transposition(text1, 3)
    print(f"clue 1: {enc1}")
    enc2 = encrypt_transposition_with_secret(text2, 3, 213 )
    print(f"clue 2: {enc2}")
    enc3 = encrypt_transposition_with_secret(text3, 4, "4132")
    print(f"clue 3: {enc3}")


