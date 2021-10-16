from evaluation.core.evaluators.base import BaseEvaluator
from evaluation.core.evaluators.modes import EvaluationModes
from evaluation.results.two_class import TwoClassEvalResult


class TwoClassEvaluator(BaseEvaluator):

    def __init__(self, eval_mode=EvaluationModes.Extraction):
        super(TwoClassEvaluator, self).__init__(eval_mode=eval_mode)

    def _create_eval_result(self):
        return TwoClassEvalResult()
