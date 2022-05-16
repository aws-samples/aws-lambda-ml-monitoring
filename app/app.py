import json
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import gc
import requests
from monitor import (log_inputs_for, log_outputs_for)


def lambda_handler(event, context):
    body = json.loads(event['body'])

    question = body['question']
    context = body['context']

    log_input = [
        {"question": question,
         "context": context}
    ]

    log_inputs_for("1234", log_input)

    # Load model
    tokenizer = AutoTokenizer.from_pretrained("model/")
    model = AutoModelForQuestionAnswering.from_pretrained("model/")

    inputs = tokenizer.encode_plus(
        question, context, add_special_tokens=True, return_tensors="pt")

    input_ids = inputs["input_ids"].tolist()[0]

    output = model(**inputs)

    answer_start_scores = output.start_logits
    answer_end_scores = output.end_logits

    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    print('Question:{0}, Answer: {1}'.format(question, answer))

    # delete model and gc
    del tokenizer

    del model
    torch.cuda.empty_cache()
    gc.collect()

    # log results
    log_outputs_for("1234", [{"answer": answer}])

    return {
        'statusCode': 200,
        'body': json.dumps({
            'Question': question,
            'Answer': answer
        })
    }
