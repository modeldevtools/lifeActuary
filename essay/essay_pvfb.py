__author__ = "PedroCR"

from soa_tables import read_soa_table_xml as rst
from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
import mortality_table as mt
from multidecrement_table import MultiDecrementTable as mdt
import age
from present_value_of_future_benefits import pvtermcost
from matplotlib import pyplot as plt

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
dt_ekv80 = mt.MortalityTable(mt=ekv80, last_q=0)
tt_pcr = mt.MortalityTable(mt=pcr1, last_q=0)

tables_unidecrement = {'mortality': mt_TV7377, 'disability': dt_ekv80, 'turnover': tt_pcr}

tables_multidecrement = mdt(dict_tables=tables_unidecrement)
tables_multidecrement.create_udd_multidecrement_table()

dict_dates = {'date_of_birth': '1977-03-12', 'date_of_entry': '1997-05-15'}
date_of_valuation = '2019-12-31'

dates_for_term_cost = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(55)
age_term_cost_years = dates_for_term_cost.age_act()
pvfb_d = pvtermcost.PVTermCost(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
                               date_of_entry=dict_dates['date_of_entry'], age_of_term_cost=age_term_cost_years,
                               multi_table=tables_multidecrement, decrement='disability', i=2,
                               age_first_instalment=None, age_last_instalment=None, age_first_payment=None)

pvfb_d.set_default_waiting_periods()

# compute pvfb
x = 45
print(f"PVBT({pvfb_d.y}, {pvfb_d.x}, {pvfb_d.age_of_term_cost}|{x})={pvfb_d.pvtc(x=x)}")
print(f"PVBT({pvfb_d.y}, {pvfb_d.x}, {pvfb_d.age_of_term_cost}|{pvfb_d.x})={pvfb_d.pvtc_x()}")

pvfb_all_d = pvfb_d.pvtc_all_ages()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_d[1][:], pvfb_all_d[2][:], 'o-', label='pvfb disability')
plt.legend()

'''
test pvfb
'''

print(f"vec_PVBT={pvfb_d.vec_pvfb(x=x, age_term_cost_init=pvfb_d.y, age_term_cost_final=65, dif_age_last_instalment=1, dif_age_first_payment=0)}")
print(f"vec_PVBT={pvfb_d.vec_pvfb_x(age_term_cost_init=pvfb_d.y, age_term_cost_final=65, dif_age_last_instalment=1, dif_age_first_payment=0)}")

'''
test retirement
'''
print('\n')
print('Testing for Retirement at 65')
age_retirement_65 = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(65)
pvfb_retirement = pvtermcost.PVTermCost(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
                                        date_of_entry=dict_dates['date_of_entry'], age_of_term_cost=65,
                                        multi_table=tables_multidecrement, decrement=None, i=2,
                                        age_first_instalment=None, age_last_instalment=None, age_first_payment=None)

pvfb_retirement.set_default_waiting_periods()

# compute pvfb
x = 65
print(
    f"PVBT({pvfb_retirement.y}, {pvfb_retirement.x}, {pvfb_retirement.age_of_term_cost}|{x})={pvfb_retirement.pvtc(x=x)}")
print(
    f"PVBT({pvfb_retirement.y}, {pvfb_retirement.x}, {pvfb_retirement.age_of_term_cost}|{pvfb_retirement.x})={pvfb_retirement.pvtc_x()}")

pvfb_all_retirement = pvfb_retirement.pvtc_all_ages()
fig, ax = fig, axs = plt.subplots()
plt.plot(pvfb_all_retirement[1], pvfb_all_retirement[2], 'o-', label='pvfb retirement')
plt.legend()
