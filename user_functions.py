from translate import *

# add user input

def get_user_input():
    while True:
        # Get user input
        input_language = input("Enter the input language (or 'exit' to quit): ")
        if input_language.lower() == 'exit':
            break

        output_language = input("Enter the output language: ")
        user_text = input("Enter the text to translate: ")

        # Call the translation function
        translated_text = translate_text(user_text, input_language, output_language)

        # Display the result
        print(f"Translated text ({output_language}): {translated_text}\n")

        # Option to continue or exit
        if input("Translate another text? (y/n): ").lower() != 'y':
            break
get_user_input()