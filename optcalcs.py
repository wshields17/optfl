# import xlwings as xw
import QuantLib as ql



import py_vollib.black_scholes_merton.implied_volatility as BSvol
import py_vollib.black_scholes_merton as BSprice
import py_vollib.black_scholes_merton.greeks.analytical as BSgreeks
import py_vollib.black_scholes_merton.greeks.numerical as BSgreeksN

def double_sum(x, y):
    """Returns twice the sum of the two arguments"""
    return 2 * (x + y)


def opprice(cp,sprice,strike,timexp,inrate,vol,divr):
  price = BSprice.black_scholes_merton(cp,sprice,strike,timexp,inrate,vol,divr)   
  return price


def optheta(cp,sprice,strike,timexp,inrate,vol,divr):
  price = BSgreeksN.theta(cp,sprice,strike,timexp,inrate,vol,divr)   
  return price  


def opdelta(cp,sprice,strike,timexp,inrate,vol,divr):
  price = BSgreeksN.delta(cp,sprice,strike,timexp,inrate,vol,divr)   
  return price  

def opgamma(cp,sprice,strike,timexp,inrate,vol,divr):
  price = BSgreeksN.gamma(cp,sprice,strike,timexp,inrate,vol,divr)   
  return price  


def opvega(cp,sprice,strike,timexp,inrate,vol,divr):
  price = BSgreeksN.vega(cp,sprice,strike,timexp,inrate,vol,divr)   
  return price        


def opvol(oprice,sprice,strike,timexp,inrate,divr,cp):
  price = BSvol.implied_volatility(oprice,sprice,strike,timexp,inrate,divr,cp)   
  return price
  
def binomialmodels(stockprice,strikeprice,volatility,intrate,calcdate,expdate,divrate,opttype):
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates()  
    modelname = 'crr'
    steps = 501
    
    calculation_date = ql.Date(calcdate.day, calcdate.month,calcdate.year)
    if opttype == "p":
        option_type = ql.Option.Put
    else:
        option_type = ql.Option.Call    
    exp_date = ql.Date(expdate.day,expdate.month,expdate.year)
    ql.Settings.instance().evaluationDate = calculation_date
    payoff = ql.PlainVanillaPayoff(option_type, strikeprice)
    exercise = ql.AmericanExercise(calculation_date,exp_date)
    american_option = ql.VanillaOption(payoff, exercise)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(stockprice))

    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, intrate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, divrate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    binomial_engine = ql.BinomialVanillaEngine(bsm_process, modelname, steps)
    american_option.setPricingEngine(binomial_engine)
    
    return american_option.NPV()


print("ok")

    
