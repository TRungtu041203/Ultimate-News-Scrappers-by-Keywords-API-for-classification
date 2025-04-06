import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv

from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Initialize Gemini LLM via LlamaIndex
llm = Gemini(
    api_key=GOOGLE_API_KEY,
    model="models/gemini-2.0-flash",
    temperature=0.0,
    max_tokens=2000
)
Settings.llm = llm

def categorize_articles_batch(articles):
    """
    Categorizes up to 15 articles at once using Gemini via LlamaIndex.
    """
    system_prompt = (
        "You are an expert Vietnamese game-related news categorizer. Your task is to assign categories to each article below "
        "based solely on the content. For each article, return a line with its index followed by a colon and the category result.\n\n"
        "You must choose one or more from the following:\n"
        "1. 'Tổng quan ngành video games tại Việt Nam': Articles that provide a general overview or background of the video game industry in Vietnam.\n"
        "2. 'Việc phát triển games tại Việt Nam, green gaming, và bảo vệ môi trường': Articles discussing the development of games in Vietnam with an emphasis on environmental sustainability, including topics like green gaming or environmental protection initiatives.\n"
        "3. 'Việc phát triển games và sử dụng công cụ AIs': Articles related to the development of video games and/or the use of artificial intelligence tools in game creation or gameplay.\n"
        "4. 'Esports in Vietnam': Articles focused on competitive gaming, esports events, or the esports industry within Vietnam.\n\n"
        "If no categories apply to a specific article, return 'None'.\n"
        "Output format:\n0: <category result>\n1: <category result>\n...\n\n"
    )

    article_block = ""
    for i, article_text in enumerate(articles):
        article_block += f"Article {i}:\n{article_text.strip()}\n\n"

    user_prompt = f"{system_prompt}Here are the articles:\n\n{article_block}"

    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt)
    ]

    try:
        response = llm.chat(messages)
        raw_output = response.message.content.strip()
        print("Raw model output:\n", raw_output)
        # Parse output like: 0: Category A\n1: Category B\n...
        result_lines = raw_output.splitlines()
        results = {}
        for line in result_lines:
            if ':' in line:
                index, cats = line.split(':', 1)
                results[int(index.strip())] = cats.strip()
        return results
    except Exception as e:
        print("Error during batch categorization:", e)
        return {i: "None" for i in range(len(articles))}

def main(input_csv, output_csv):
    articles = []
    with open(input_csv, newline='', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            articles.append(row)

    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as fout:
        fieldnames = list(articles[0].keys()) + ["Categories"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for start_idx in range(0, len(articles), 15):
            batch = articles[start_idx:start_idx + 15]
            print(f"\n🔄 Processing batch {start_idx} to {start_idx + len(batch) - 1}...")

            combined_texts = []
            for article in batch:
                parts = [article.get("Title", ""), article.get("Summary", "")]
                combined_text = "\n".join(parts)
                combined_texts.append(combined_text)

            batch_results = categorize_articles_batch(combined_texts)

            for i, article in enumerate(batch):
                article["Categories"] = batch_results.get(i, "None")
                writer.writerow(article)
                fout.flush()

            # Optional pause to avoid flooding API
            time.sleep(1)

    print(f"\n✅ Categorization completed. Results saved to {output_csv}")

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv_file = f"categorized_articles_{timestamp}.csv"
    input_csv_file = r"D:\Data\vietnews\output\motgame_20250404_174106 - Copy.csv"
    output_csv_file = os.path.join(r"D:\Data\vietnews\output", output_csv_file)

    main(input_csv_file, output_csv_file)
