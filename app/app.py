import json
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
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

    question_answerer = pipeline(
        "question-answering", model=model, tokenizer=tokenizer)

    output = question_answerer(question=question, context=context)

    print(output)

    # delete model and gc
    del tokenizer

    del model
    torch.cuda.empty_cache()
    gc.collect()

    # log results
    log_outputs_for("1234", [{"output": output}])

    return {
        'statusCode': 200,
        'body': json.dumps({
            'Question': question,
            'Answer': output["answer"],
            'score': output["score"]
        })
    }
