import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function 
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini api key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        function_responses = []

        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions]),
                            )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        if response.function_calls != None:
            for obj in response.function_calls:
                function_call_result = call_function(obj, args.verbose)
                if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                        or not function_call_result.parts[0].function_response.response
                    ):
                    raise RuntimeError(f"Empty function response for {obj.name}")

                function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(types.Content(role="user", parts=function_responses))

        else:
            print(response.text)
            return

    print("Maximum number of 20 itterations reached. Task failed")
    sys.exit(1)


if __name__ == "__main__":
    main()
