import os
import getpass
import argparse
from agents import GeneratorAgent

generator_sys_init = """You are a helpful assistant that extracts and refines knowledge from a given text.
Your goal is to identify key concepts, principles, and factual information.
While examples can be useful for understanding, they should not be the primary focus.
Instead, prioritize the underlying knowledge that the examples are intended to illustrate.
However, do not completely ignore examples as they can provide context and aid in understanding complex ideas."""

generator = GeneratorAgent("gpt-3.5-turbo", generator_sys_init, 1000)

def read_text_file_in_segments(filename, buffer_size, overlap_size):
    with open(filename, 'r') as f:
        overlap = ''
        while True:
            buffer = f.read(buffer_size)
            if not buffer:
                break
            yield overlap + buffer
            overlap = buffer[-overlap_size:]
            if len(buffer) < buffer_size:
                break
            f.seek(f.tell() - overlap_size)

def extract_relevant_content(content):
    try:
        response = generator(content)  # Replace with your GPT function call
        return response
    except Exception as e:
        print(f"Error in content extraction: {str(e)}")
        return ""

def process_and_save(file_path, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for segment in read_text_file_in_segments(file_path, 2000, 200):
            extracted_content = extract_relevant_content(segment)
            output_file.write(extracted_content + "\n\n----------\n\n")

def main():
    if 'OPENAI_API_KEY' not in os.environ:
        os.environ['OPENAI_API_KEY'] = getpass.getpass('Please enter your API key: ')

    parser = argparse.ArgumentParser(description="Process a text file and generate relevant content.")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to the output text file")
    
    args = parser.parse_args()

    process_and_save(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
