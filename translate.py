# Import prerequisite libraries
import os
import openai

# Setting the API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Perform tasks using OpenAI API
# model options
print(openai.Model.list())

def translate_text(text, input_language, output_language):
    prompt = f"Translate the following '{input_language}' text to '{output_language}': {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your job is to accurately translate the input text from the input langauage to the specfified output language. Your main priority is to maintain meaning, tone, and context with high accuracy. Do not add anythin outside of that."},
            {"role": "user", "content": prompt}
        ],
        # this could be too short but want to ensure low cost
        max_tokens=1500,
        n=1,
        stop=None,
        # temp param controls the randomness of the output. A lower temperature results in more predictable translations. 0.5 seems appropriate when trying to translate accurately
        temperature=0.5,
    )
    # parsing and setting the response output to translation
    translation = response.choices[0].message.content.strip()
    return translation


# test with different pairs to see results
# keep language names to their english translation
def test():
    input_language = "English"
    output_languages = ["Portugese", "Japanese", "French"]
    test_texts = ["Hello, how are you doing?", "I like to eat ice cream on sunny days in the summer.", "I like my coffee in one specific way: black."]
    for text in test_texts:
        print(f"Original text ({input_language}): {text}")
        for language in output_languages:
            translated_text = translate_text(text, input_language, language)
            print(f"Translated into {language}: {translated_text}")
        # adding space for next test text
        print("\n" + "-"*50 + "\n")

test()