from sklearn import metrics


def regression_metrics(y_true, y_pred):
    max_error = metrics.max_error(y_true, y_pred)
    mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred)
    mean_squared_error = metrics.mean_squared_error(y_true, y_pred)
    mean_squared_log_error = metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error = metrics.median_absolute_error(y_true, y_pred)
    r2_score = metrics.r2_score(y_true, y_pred)
    mean_poisson_deviance = metrics.mean_poisson_deviance(y_true, y_pred)
    mean_gamma_deviance = metrics.mean_gamma_deviance(y_true, y_pred)
    mean_tweedie_deviance = metrics.mean_tweedie_deviance(y_true, y_pred)
    # create dictionary of metrics
    metrics_dict = {
        "max_error": max_error,
        "mean_absolute_error": mean_absolute_error,
        "mean_squared_error": mean_squared_error,
        "mean_squared_log_error": mean_squared_log_error,
        "median_absolute_error": median_absolute_error,
        "r2_score": r2_score,
        "mean_poisson_deviance": mean_poisson_deviance,
        "mean_gamma_deviance": mean_gamma_deviance,
        "mean_tweedie_deviance": mean_tweedie_deviance,
    }
    return metrics_dict


def classification_metrics(y_true, y_pred):
    accuracy_score = metrics.accuracy_score(y_true, y_pred)
    balanced_accuracy_score = metrics.balanced_accuracy_score(y_true, y_pred)
    cohen_kappa_score = metrics.cohen_kappa_score(y_true, y_pred)
    f1_score = metrics.f1_score(y_true, y_pred)
    fbeta_score = metrics.fbeta_score(y_true, y_pred,beta=0.5)
    hamming_loss = metrics.hamming_loss(y_true, y_pred)
    jaccard_score = metrics.jaccard_score(y_true, y_pred)
    log_loss = metrics.log_loss(y_true, y_pred)
    matthews_corrcoef = metrics.matthews_corrcoef(y_true, y_pred)
    precision_score = metrics.precision_score(y_true, y_pred)
    recall_score = metrics.recall_score(y_true, y_pred)
    zero_one_loss = metrics.zero_one_loss(y_true, y_pred)
    # create dictionary of metrics
    metrics_dict = {
        "accuracy_score": accuracy_score,
        "balanced_accuracy_score": balanced_accuracy_score,
        "cohen_kappa_score": cohen_kappa_score,
        "f1_score": f1_score,
        "fbeta_score": fbeta_score,
        "hamming_loss": hamming_loss,
        "jaccard_score": jaccard_score,
        "log_loss": log_loss,
        "matthews_corrcoef": matthews_corrcoef,
        "precision_score": precision_score,
        "recall_score": recall_score,
        "zero_one_loss": zero_one_loss,
    }
    return metrics_dict


def log_metrics(y_true, y_pred, task):
    if task == "regression":
        metrics_dict = regression_metrics(y_true, y_pred)
        return metrics_dict
    elif task == "classification":
        metrics_dict = classification_metrics(y_true, y_pred)
        return metrics_dict


