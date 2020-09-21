import numpy as np
from ....utils.model_wrapper import model_wrapper_for_ta


def create_ta_recipe(model, tokenizer, recipe):
    """

    :param model:
    :param tokenizer:
    :param recipe: str for built-in recipes, how to
    :return:
    """
    # model wrapper
    wrapper = model_wrapper_for_ta(model, tokenizer)
    # build attack
    import textattack.attack_recipes as ta_recipes
    if isinstance(recipe, str):
        recipe = getattr(ta_recipes, recipe)
    else:
        raise ValueError("only supports built-in recipes")
    attack = recipe.build(wrapper)
    return attack


def run_ta_test(attack, data):

    # get logger
    from textattack.loggers import AttackLogManager
    logger = AttackLogManager()
    logger.enable_stdout()
    # run attack
    result = list(attack.attack_dataset(data))
    logger.log_results(result)

    return logger


def get_result_from_logger(logger):
    total_attacks = len(logger.results)
    if total_attacks == 0:
        return
    # Count things about attacks.
    all_num_words = np.zeros(len(logger.results))
    perturbed_word_percentages = np.zeros(len(logger.results))
    num_words_changed_until_success = np.zeros(
        2 ** 16
    )  # @ TODO: be smarter about this
    failed_attacks = 0
    skipped_attacks = 0
    successful_attacks = 0
    max_words_changed = 0
    attacks_with_additional_grammar_errors = 0
    from textattack.constraints.grammaticality.language_tool import LanguageTool
    language_tool = LanguageTool()
    from textattack.attack_results import FailedAttackResult, SkippedAttackResult
    for i, result in enumerate(logger.results):
        all_num_words[i] = len(result.original_result.attacked_text.words)
        if isinstance(result, FailedAttackResult):
            failed_attacks += 1
            continue
        elif isinstance(result, SkippedAttackResult):
            skipped_attacks += 1
            continue
        else:
            successful_attacks += 1
        num_words_changed = len(
            result.original_result.attacked_text.all_words_diff(
                result.perturbed_result.attacked_text
            )
        )
        num_words_changed_until_success[num_words_changed - 1] += 1
        max_words_changed = max(
            max_words_changed or num_words_changed, num_words_changed
        )
        if len(result.original_result.attacked_text.words) > 0:
            perturbed_word_percentage = (
                    num_words_changed
                    * 100.0
                    / len(result.original_result.attacked_text.words)
            )
        else:
            perturbed_word_percentage = 0
        perturbed_word_percentages[i] = perturbed_word_percentage
        if not language_tool._check_constraint(result.perturbed_result.attacked_text,
                                               result.original_result.attacked_text):
            attacks_with_additional_grammar_errors += 1


    # Original classifier success rate on these samples.
    original_accuracy = (total_attacks - skipped_attacks) * 100.0 / (total_attacks)
    # original_accuracy = str(round(original_accuracy, 2)) + "%"

    # New classifier success rate on these samples.
    accuracy_under_attack = (failed_attacks) * 100.0 / (total_attacks)
    # accuracy_under_attack = str(round(accuracy_under_attack, 2)) + "%"

    # Attack success rate.
    if successful_attacks + failed_attacks == 0:
        attack_success_rate = 0
    else:
        attack_success_rate = (
                successful_attacks * 100.0 / (successful_attacks + failed_attacks)
        )
    # attack_success_rate = str(round(attack_success_rate, 2)) + "%"

    perturbed_word_percentages = perturbed_word_percentages[
        perturbed_word_percentages > 0
        ]
    average_perc_words_perturbed = perturbed_word_percentages.mean()
    # average_perc_words_perturbed = str(round(average_perc_words_perturbed, 2)) + "%"

    average_num_words = all_num_words.mean()
    # average_num_words = str(round(average_num_words, 2))

    additional_grammar_errors_pctg = attacks_with_additional_grammar_errors * 100.0 / (total_attacks)

    summary_table_rows = {
        "Number of successful attacks": successful_attacks,
        "Number of failed attacks": failed_attacks,
        "Number of skipped attacks": skipped_attacks,
        "Original accuracy": original_accuracy,
        "Accuracy under attack": accuracy_under_attack,
        "Attack success rate": attack_success_rate,
        "Average perturbed word %": average_perc_words_perturbed,
        "Average num. words per input": average_num_words,
    }

    num_queries = np.array(
        [
            r.num_queries
            for r in logger.results
            if not isinstance(r, SkippedAttackResult)
        ]
    )
    avg_num_queries = num_queries.mean()
    # avg_num_queries = str(round(avg_num_queries, 2))
    summary_table_rows.update({"Avg num queries:": avg_num_queries,
                               "(Additional) grammar error rate": additional_grammar_errors_pctg,})

    return summary_table_rows
