import logging
from typing import Any

import bert_score

from src.moonshot.src.utils.timeit import timeit

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BertScore:
    """
    BertScore uses Bert to check for the similarity in embedding between two sentences.
    Code reference from:
    https://github.com/Tiiiger/bert_score/blob/master/bert_score_cli/score.py
    """

    @staticmethod
    @timeit
    def get_results(
        prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Calculate the BERTScore precision, recall, and F1 score between the predicted results and the target results.

        Parameters:
            prompts (Any): The prompts used for generating the predicted results.
            predicted_results (Any): The predicted results generated by the model.
            targets (Any): The target results for comparison.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: A dictionary containing the BERTScore precision, recall, and F1 score.
                - precision (float): The precision score.
                - recall (float): The recall score.
                - f1 (float): The F1 score.
        """
        # use default roberto model
        score = bert_score.score(
            predicted_results,
            targets,
            lang="en",
        )

        avg_scores = [s.mean(dim=0) for s in score]
        precision_value = avg_scores[0].cpu().item()
        recall_value = avg_scores[1].cpu().item()
        f1_value = avg_scores[2].cpu().item()
        return {
            "bertscore": {
                "precision": precision_value,
                "recall": recall_value,
                "f1": f1_value,
            }
        }
