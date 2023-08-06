import datetime

import numpy as np
import pandas as pd

import numpyro
import numpyro.distributions as dist
from numpyro.contrib.control_flow import scan
from numpyro.infer import MCMC, NUTS, Predictive

import jax.numpy as jnp
import jax.random as random
from numpyro.infer import MCMC, NUTS, Predictive

import scenario_generator.utils as u

# https://num.pyro.ai/en/stable/tutorials/time_series_forecasting.html 
def sgt(y, seasonality, future=0):
    """
    TODO!
    """

    # heuristically, standard derivation of Cauchy prior depends on
    # the max value of data
    cauchy_sd = jnp.max(y) / 150
    # NB: priors' parameters are taken from
    # https://github.com/cbergmeir/Rlgt/blob/master/Rlgt/R/rlgtcontrol.R
    nu = numpyro.sample("nu", dist.Uniform(2, 20))
    powx = numpyro.sample("powx", dist.Uniform(0, 1))
    sigma = numpyro.sample("sigma", dist.HalfCauchy(cauchy_sd))
    offset_sigma = numpyro.sample(
        "offset_sigma", dist.TruncatedCauchy(low=1e-10, loc=1e-10, scale=cauchy_sd)
    )

    coef_trend = numpyro.sample("coef_trend", dist.Cauchy(0, cauchy_sd))
    pow_trend_beta = numpyro.sample("pow_trend_beta", dist.Beta(1, 1))
    # pow_trend takes values from -0.5 to 1
    pow_trend = 1.5 * pow_trend_beta - 0.5
    pow_season = numpyro.sample("pow_season", dist.Beta(1, 1))

    level_sm = numpyro.sample("level_sm", dist.Beta(1, 2))
    s_sm = numpyro.sample("s_sm", dist.Uniform(0, 1))
    init_s = numpyro.sample("init_s", dist.Cauchy(0, y[:seasonality] * 0.3))

    def transition_fn(carry, t):
        level, s, moving_sum = carry
        season = s[0] * level**pow_season
        exp_val = level + coef_trend * level**pow_trend + season
        exp_val = jnp.clip(exp_val, a_min=0)
        # use expected vale when forecasting
        y_t = jnp.where(t >= N, exp_val, y[t])

        moving_sum = (
            moving_sum + y[t] - jnp.where(t >= seasonality, y[t - seasonality], 0.0)
        )
        level_p = jnp.where(t >= seasonality, moving_sum / seasonality, y_t - season)
        level = level_sm * level_p + (1 - level_sm) * level
        level = jnp.clip(level, a_min=0)

        new_s = (s_sm * (y_t - level) / season + (1 - s_sm)) * s[0]
        # repeat s when forecasting
        new_s = jnp.where(t >= N, s[0], new_s)
        s = jnp.concatenate([s[1:], new_s[None]], axis=0)

        omega = sigma * exp_val**powx + offset_sigma
        y_ = numpyro.sample("y", dist.StudentT(nu, exp_val, omega))

        return (level, s, moving_sum), y_

    N = y.shape[0]
    level_init = y[0]
    s_init = jnp.concatenate([init_s[1:], init_s[:1]], axis=0)
    moving_sum = level_init
    with numpyro.handlers.condition(data={"y": y[1:]}):
        _, ys = scan(
            transition_fn, (level_init, s_init, moving_sum), jnp.arange(1, N + future)
        )
    if future > 0:
        numpyro.deterministic("y_forecast", ys[-future:])


def mcmc_predict(y_train: jnp.array,
                 forecast_length: int,
                 num_warmup_mcmc: int = 500,
                 num_samples_mcmc: int = 100,
                 seasonality_mcmc: int = 1000,
                 num_chains_mcmc: int = 2,
                 verbose: bool = True):
    kernel = NUTS(sgt)
    mcmc = MCMC(kernel, num_warmup=num_warmup_mcmc, num_samples=num_samples_mcmc, num_chains=num_chains_mcmc)
    mcmc.run(random.PRNGKey(0), y_train, seasonality=seasonality_mcmc)
    if verbose:
        mcmc.print_summary()
    samples = mcmc.get_samples()

    predictive = Predictive(sgt, samples, return_sites=["y_forecast"])
    predict_dist = predictive(random.PRNGKey(1), y_train, seasonality=seasonality_mcmc, future=forecast_length)[
        "y_forecast"
    ]
    return predict_dist


def forecast_rb_onboard_power(train_start_date: datetime.date, 
                              train_end_date: datetime.date,
                              forecast_length: int,
                              num_warmup_mcmc: int = 500,
                              num_samples_mcmc: int = 100,
                              seasonality_mcmc: int = 1000,
                              num_chains_mcmc: int = 2):
    u.sanity_check_date(train_start_date, err_msg="Specified train_start_date is after today!")
    u.sanity_check_date(train_end_date, err_msg="Specified train_end_date is after today!")

    x, y = u.get_historical_daily_onboarded_power(train_start_date, train_end_date)
    y_train = jnp.array(y)
    u.err_check_train_data(y_train)
    
    # y_scale = y_train.max()
    y_scale = 1
    rb_onboard_power_pred = mcmc_predict(y_train/y_scale, forecast_length,
                                         num_warmup_mcmc=num_warmup_mcmc, 
                                         num_samples_mcmc=num_samples_mcmc,
                                         seasonality_mcmc=seasonality_mcmc, 
                                         num_chains_mcmc=num_chains_mcmc)
    rb_onboard_power_pred *= y_scale
    
    forecast_start_date = train_end_date + datetime.timedelta(days=1)
    forecast_date_vec = u.make_forecast_date_vec(forecast_start_date, forecast_length)
    return forecast_date_vec, rb_onboard_power_pred, x, y

"""
TODO: check on this, for now we use offline data
####### forecast renewal rate
sector_expirations_df = query_starboard_sector_expirations(start_date, current_date)
df_extend_subset = sector_expirations_df.copy()

### predict extensions
y_train_extend = jnp.clip(jnp.array(df_extend_subset['extended_rb'].values), a_min=0.01, a_max=None)[-num_days_train:]
forecast_extend = mcmc_predict(y_train_extend, forecast_length)

####### forecast expirations
y_train_expire = jnp.clip(jnp.array(df_extend_subset['expired_rb'].values), a_min=0.01, a_max=None)[-num_days_train:]
forecast_expire = mcmc_predict(y_train_expire, forecast_length)
"""
def forecast_extensions(train_start_date: datetime.date, 
                        train_end_date: datetime.date,
                        forecast_length: int,
                        num_warmup_mcmc: int = 500,
                        num_samples_mcmc: int = 100,
                        seasonality_mcmc: int = 1000,
                        num_chains_mcmc: int = 2):
    u.sanity_check_date(train_start_date, err_msg="Specified train_start_date is after today!")
    u.sanity_check_date(train_end_date, err_msg="Specified train_end_date is after today!")

    x, y = u.get_historical_extensions(train_start_date, train_end_date)
    y_train = jnp.array(y)
    u.err_check_train_data(y_train)

    extensions_pred = mcmc_predict(y_train, forecast_length,
                                   num_warmup_mcmc=num_warmup_mcmc, 
                                   num_samples_mcmc=num_samples_mcmc,
                                   seasonality_mcmc=seasonality_mcmc, 
                                   num_chains_mcmc=num_chains_mcmc)
    
    forecast_start_date = train_end_date + datetime.timedelta(days=1)
    forecast_date_vec = u.make_forecast_date_vec(forecast_start_date, forecast_length)
    return forecast_date_vec, extensions_pred, x, y

def forecast_expirations(train_start_date: datetime.date, 
                         train_end_date: datetime.date,
                         forecast_length: int,
                         num_warmup_mcmc: int = 500,
                         num_samples_mcmc: int = 100,
                         seasonality_mcmc: int = 1000,
                         num_chains_mcmc: int = 2):
    u.sanity_check_date(train_start_date, err_msg="Specified train_start_date is after today!")
    u.sanity_check_date(train_end_date, err_msg="Specified train_end_date is after today!")

    x, y = u.get_historical_expirations(train_start_date, train_end_date)
    y_train = jnp.array(y)
    u.err_check_train_data(y_train)

    expire_pred = mcmc_predict(y_train, forecast_length,
                               num_warmup_mcmc=num_warmup_mcmc, 
                               num_samples_mcmc=num_samples_mcmc,
                               seasonality_mcmc=seasonality_mcmc, 
                               num_chains_mcmc=num_chains_mcmc)
    
    forecast_start_date = train_end_date + datetime.timedelta(days=1)
    forecast_date_vec = u.make_forecast_date_vec(forecast_start_date, forecast_length)
    return forecast_date_vec, expire_pred, x, y

def forecast_renewal_rate(train_start_date: datetime.date, 
                          train_end_date: datetime.date,
                          forecast_length: int,
                          num_warmup_mcmc: int = 500,
                          num_samples_mcmc: int = 100,
                          seasonality_mcmc: int = 1000,
                          num_chains_mcmc: int = 2):
    u.sanity_check_date(train_start_date, err_msg="Specified train_start_date is after today!")
    u.sanity_check_date(train_end_date, err_msg="Specified train_end_date is after today!")

    forecast_date_vec, extensions_pred, x_extend, y_extend = forecast_extensions(train_start_date, 
                                                                                 train_end_date,
                                                                                 forecast_length,
                                                                                 num_warmup_mcmc = num_warmup_mcmc,
                                                                                 num_samples_mcmc = num_samples_mcmc,
                                                                                 seasonality_mcmc = seasonality_mcmc,
                                                                                 num_chains_mcmc = num_chains_mcmc)
    _, expire_pred, x_expire, y_expire = forecast_expirations(train_start_date, 
                                                              train_end_date,
                                                              forecast_length,
                                                              num_warmup_mcmc = num_warmup_mcmc,
                                                              num_samples_mcmc = num_samples_mcmc,
                                                              seasonality_mcmc = seasonality_mcmc,
                                                              num_chains_mcmc = num_chains_mcmc)
    if not x_extend.equals(x_expire):
        raise ValueError("Unable to get the same amount of data for extensions and expirations!")
    renewal_rate_historical = y_extend / (y_extend + y_expire)

    renewal_rate_pred = extensions_pred / (extensions_pred + expire_pred)
    return forecast_date_vec, renewal_rate_pred, x_extend, renewal_rate_historical


def forecast_filplus_rate(train_start_date: datetime.date, 
                          train_end_date: datetime.date,
                          forecast_length: int,
                          num_warmup_mcmc: int = 500,
                          num_samples_mcmc: int = 100,
                          seasonality_mcmc: int = 1000,
                          num_chains_mcmc: int = 2):
    """
    1. forecast deal_onboard --> deal_onboard_dist
    2. find cc_onboard = rawbyte_onboard - deal_onboard
    3. forecast cc_onboard --> cc_onboard_dist
    4. find fil_plus_rate_dist =  deal_onboard_dist / (cc_onboard_dist + deal_onboard_dist)
    """
    u.sanity_check_date(train_start_date, err_msg="Specified train_start_date is after today!")
    u.sanity_check_date(train_end_date, err_msg="Specified train_end_date is after today!")

    x_deal_onboard_train, y = u.get_historical_deals_onboard(train_start_date, train_end_date)
    y_deal_onboard_train = jnp.array(y)
    u.err_check_train_data(y_deal_onboard_train)

    x_rb_onboard_train, y_rb_onboard_train = \
        u.get_historical_daily_onboarded_power(train_start_date, train_end_date)
    train_start_date = pd.to_datetime(max(x_deal_onboard_train.values[0], x_rb_onboard_train.values[0]))
    train_end_date = pd.to_datetime(min(x_deal_onboard_train.values[-1], x_rb_onboard_train.values[-1]))

    ii_start = np.where(train_start_date==x_rb_onboard_train.values)[0][0]
    ii_end = np.where(train_end_date==x_rb_onboard_train.values)[0][0]
    x_rb_onboard_train = x_rb_onboard_train[ii_start:ii_end]
    y_rb_onboard_train = y_rb_onboard_train[ii_start:ii_end]

    ii_start = np.where(train_start_date==x_deal_onboard_train.values)[0][0]
    ii_end = np.where(train_end_date==x_deal_onboard_train.values)[0][0]
    x_deal_onboard_train = x_deal_onboard_train[ii_start:ii_end]
    y_deal_onboard_train = y_deal_onboard_train[ii_start:ii_end]

    # y_deal_onboard_scale = y_deal_onboard_train.max()
    y_deal_onboard_scale = 1
    deal_onboard_pred = mcmc_predict(y_deal_onboard_train/y_deal_onboard_scale, forecast_length,
                                     num_warmup_mcmc=num_warmup_mcmc, 
                                     num_samples_mcmc=num_samples_mcmc,
                                     seasonality_mcmc=seasonality_mcmc, 
                                     num_chains_mcmc=num_chains_mcmc)
    forecast_start_date = train_end_date + datetime.timedelta(days=1)
    forecast_date_vec = u.make_forecast_date_vec(forecast_start_date, forecast_length)
    deal_onboard_pred *= y_deal_onboard_scale

    y_cc_onboard_train = jnp.array(y_rb_onboard_train - y_deal_onboard_train)
    # y_cc_onboard_scale = y_cc_onboard_train.max()
    y_cc_onboard_scale = 1
    cc_onboard_pred = mcmc_predict(y_cc_onboard_train/y_cc_onboard_scale, forecast_length,
                                   num_warmup_mcmc=num_warmup_mcmc, 
                                   num_samples_mcmc=num_samples_mcmc,
                                   seasonality_mcmc=seasonality_mcmc, 
                                   num_chains_mcmc=num_chains_mcmc)
    cc_onboard_pred *= y_cc_onboard_scale

    xx = x_rb_onboard_train
    yy = y_deal_onboard_train / (y_cc_onboard_train + y_deal_onboard_train)
    filplus_rate_pred = deal_onboard_pred / (cc_onboard_pred + deal_onboard_pred)
    return forecast_date_vec, filplus_rate_pred, xx, yy

