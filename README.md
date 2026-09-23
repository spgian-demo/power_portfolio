# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 5.2: Price Sensitivity of Market Cash Flows.

## Current baseline

The existing main.py still prints the same 48-period report
for 2026-09-01 using seed 42. Its market cash flow remains -437.28 GBP.
The generator, portfolio class, financial formulas and time helpers are
unchanged from the preceding checkpoint.

## Lecture 5.1 examples retained

price_examples.py first prints the six original single-period cases.
Their numerical results are unchanged. They compare a 2 MWh shortage and
surplus at 80, 0 and -20 GBP/MWh.  

## Lecture 5.2 comparison

The script then compares three alternative versions of ONE day:
original prices, every price 20 GBP/MWh lower, and every price 20 GBP/MWh
higher. All shifts are relative to the original dataset, not cumulative.

Wind generation, solar generation and customer consumption are identical
in every case. The same price applies to purchases and sales within each
period. No transactions, payment dates, assets or contracts are added.
The scenarios revalue the modelled purchases and sales; they do not change
payments already agreed or represent mark-to-market valuation of contracts.

shift_wholesale_prices copies each input dictionary before changing its
price. It does not mutate the baseline. Only finite numeric shifts are
accepted, and negative resulting prices are not clipped or removed.
The caller still supplies valid energy/price records, as in the earlier model.

| Case | Price shift GBP/MWh | Buy MWh | Sell MWh | Net cash GBP | Change GBP |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 0 | 62.67 | 79.81 | -437.28 | 0.00 |
| Prices lower | -20 | 62.67 | 79.81 | -780.08 | -342.80 |
| Prices higher | +20 | 62.67 | 79.81 | -94.48 | +342.80 |

Values are rounded for display, not before the calculation.
For a UNIFORM additive price shift with fixed volumes, the cash-flow change
is (total sales - total purchases) multiplied by the shift. Here that is
(79.81 - 62.67) * 20 = +342.80 GBP for a +20 GBP/MWh shift.
This change is not the new total cash flow and is not complete profit.

This identity does not make daily netting a valid replacement for the
period calculations. For non-uniform changes, the effect depends on each
period's net position and its own price change.

This is a controlled sensitivity exercise, not a forecast, probability
model, hedge, market-risk estimate, strategy backtest or optimisation.

## Run in the existing macOS project

There are no new third-party dependencies, source modules or test modules.

## Git checkpoint

Review and stage only price_examples.py, test_main.py and README.md.
Suggested commit: Add daily wholesale price sensitivity examples
Continue on the existing branch and push the checked checkpoint.