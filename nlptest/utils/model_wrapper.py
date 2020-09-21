from transformers import DistilBertForSequenceClassification, DistilBertTokenizer, TextClassificationPipeline
import torch


def model_wrapper(model, tokenizer):
    if isinstance(model, DistilBertForSequenceClassification) and \
            isinstance(tokenizer, DistilBertTokenizer):
        # TODO: add device used to log
        device = 0 if torch.cuda.is_available() else -1
        pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, device=device,
                                              return_all_scores=True)
        return pipeline
    else:
        raise ValueError('model or tokenizer class not supported')


def model_wrapper_for_ta(model, tokenizer):
    if isinstance(model, DistilBertForSequenceClassification) and \
            isinstance(tokenizer, DistilBertTokenizer):
        from textattack.models.wrappers.huggingface_model_wrapper import HuggingFaceModelWrapper
        pipeline = HuggingFaceModelWrapper(model=model, tokenizer=tokenizer)
        return pipeline
    else:
        raise ValueError('model or tokenizer class not supported')