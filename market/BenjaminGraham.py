import yahoo_fin.stock_info as si
import pandas as pd
from StockData import StockData
from datetime import datetime
from dateutil.relativedelta import relativedelta
from json import decoder
from time import sleep
import finnhub


class GrahamFund:
    def __init__(self, st_date, nd_date, aaa_bnd_rate, out_path=r'/Users/rakeenrouf/market/data/GrahamFund'):
        self.sd = StockData(st_date, nd_date, aaa_bnd_rate)
        self.out_path = out_path

    def get_all_sp_500_stocks_stats(self):
        stocks = si.tickers_sp500()
        res_df = pd.DataFrame()
        for i, s in enumerate(stocks):
            run = True
            res = None
            while run:
                try:
                    try:
                        print(i, s)
                        if i < 0:
                            continue
                        try:
                            res = self.sd.get_tick_stats(s)
                        except ValueError:
                            res = False

                        print(res)
                    except decoder.JSONDecodeError:
                        sleep(12)
                        print(s)
                        res = self.sd.get_tick_stats(s)
                        print(res)
                    except finnhub.exceptions.FinnhubAPIException:
                        sleep(120)
                        print(s)
                        res = self.sd.get_tick_stats(s)
                        print(res)

                    except TypeError:
                        sleep(60)
                        print(s)
                        res = self.sd.get_tick_stats(s)
                        print(res)

                    except IndexError:
                        sleep(120)
                        print(s)
                        res = self.sd.get_tick_stats(s)
                        print(res)

                except KeyError:
                    pass

                except ValueError:
                    continue

                except IndexError:
                    continue

                run = False
                if isinstance(res, dict):
                    res_df = res_df.append(res, ignore_index=True)

        cols = ('any_last_5_years_pe_lt_40_p_cur_pe',
                'latest_pe_twice_aaa_rate', 'div_yld_me_2_by_3_aa',
                'tbvps_lt_2_by_3_aaa', 'stock_below_2_by_3_ncav',
                'total_debt_lt_2_by_3_nvac', 'current_ratio_mt_2',
                'tot_debt_lt_2_times_ncac',
                'annual_compound_eps_growth_rate_mt_7_percent',
                'lt_2_declines_in_eps_mt_neg_5_percent')

        d = None
        for col in cols:
            d += res_df[col]

        res_df['#_Positives'] = d
        res_df.to_csv(r'{}/{}.csv'.format(self.out_path, self.sd.end_date))
        print('Completed')


if __name__ == '__main__':
    # todo: just output what you have on failure
    end_date = datetime.today()
    start_date = end_date - relativedelta(days=365*5)

    gf = GrahamFund(start_date, end_date, aaa_bnd_rate=2.67)
    gf.get_all_sp_500_stocks_stats()
