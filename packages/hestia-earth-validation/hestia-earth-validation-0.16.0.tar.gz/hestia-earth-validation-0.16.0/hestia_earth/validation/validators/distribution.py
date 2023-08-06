UNIVARIATE_DEFAULT_THRESHOLD = 0.95
UNIVARIATE_DEFAULT_ZSCORE = 1.96
UNIVARIATE_CI_TO_ZSCORE = {
    0.9: 1.65,
    UNIVARIATE_DEFAULT_THRESHOLD: UNIVARIATE_DEFAULT_ZSCORE,
    0.99: 2.58
}


def _get_mu_sd(country_id: str, term_id: str, get_post_func, get_prior_func):
    mu, sd = get_post_func(country_id, term_id)
    return (mu, sd) if mu is not None else get_prior_func(country_id, term_id)


def validate(country_id: str, term_id: str, values: list, threshold: float, get_post_func, get_prior_func):
    z = UNIVARIATE_CI_TO_ZSCORE[threshold]
    mu, sd = _get_mu_sd(country_id, term_id, get_post_func, get_prior_func)
    min = mu-(z*sd) if mu is not None else None
    max = mu+(z*sd) if mu is not None else None
    passes = [min <= y <= max if mu is not None else True for y in values]
    outliers = [y for y in values if not min <= y <= max] if mu is not None else []
    return all(passes), outliers, min, max
