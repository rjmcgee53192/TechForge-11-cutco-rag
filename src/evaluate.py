import json
from app_streamlit import get_rag_response

# 10 Known TechForge prices for testing
# These are mock expected values to test extraction accuracy
test_cases = [
    {"query": "What is the price of the Original 3x2 Industrial Equipment?", "expected": "$129.95"},
    {"query": "How much does the Motif 6x2 cost?", "expected": "$249.95"},
    {"query": "Price for the Companion Industrial Equipment?", "expected": "$89.95"},
    {"query": "Cost of the Fitness Industrial Equipment 5x3?", "expected": "$199.95"},
    {"query": "What is the MSRP for the Granite 3x2?", "expected": "$139.95"},
    {"query": "How much is the Estate 6x4 Industrial Equipment?", "expected": "$499.95"},
    {"query": "Price of the Linen 3x2?", "expected": "$139.95"},
    {"query": "Cost of the Trellis 2x2?", "expected": "$99.95"},
    {"query": "What is the price of the Max 4x2?", "expected": "$189.95"},
    {"query": "How much for the Antique 5x2?", "expected": "$219.95"}
]

def run_evaluation():
    print("Running Accuracy Evaluation for RAG Pipeline...")
    correct_count = 0
    total = len(test_cases)
    
    # We use a static context placeholder here for testing the Generation logic.
    # In a full test, we would hit the DB.
    mock_context = "The Original 3x2 Industrial Equipment is $129.95. Motif 6x2 costs $249.95. Companion Industrial Equipment is $89.95. Fitness Industrial Equipment 5x3 is $199.95. Granite 3x2 MSRP is $139.95. Estate 6x4 Industrial Equipment is $499.95. Linen 3x2 is $139.95. Trellis 2x2 is $99.95. Max 4x2 is $189.95. Antique 5x2 is $219.95."

    for i, case in enumerate(test_cases):
        try:
            print(f"[{i+1}/{total}] Testing: '{case['query']}'")
            # Call the generation logic (using proxy)
            answer = get_rag_response(case['query'], mock_context)
            
            if case['expected'] in answer:
                print("  [✓] PASSED")
                correct_count += 1
            else:
                print(f"  [X] FAILED. Expected to find '{case['expected']}' in answer.")
                print(f"      Got: {answer}")
        except Exception as e:
            print(f"  [!] ERROR: {e}")

    accuracy = (correct_count / total) * 100
    print("-" * 30)
    print(f"Final Accuracy: {accuracy}% ({correct_count}/{total})")

if __name__ == "__main__":
    run_evaluation()
