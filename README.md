
# Basel III Output Floor Calculator

This Streamlit web app calculates the Basel III Output Floor and provides visual comparisons using both Streamlit's built-in bar chart and Matplotlib. The app allows users to input various risk-weighted assets (RWAs) and costs, and outputs whether using internal models is worth the cost compared to the standardized approach.

## Sidebar Input Parameters

1. **Credit RWAs**
   - **Description**: This input represents the risk-weighted assets (RWAs) for credit risk. It includes the total value of assets adjusted for risk, where credit risk is the risk of default by borrowers.
   - **Relation to Equation**: In the equation for calculating the output floor, the credit RWAs are part of the sum of all risk-weighted assets. Specifically, it is included in the term \((	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})\).

2. **Equity RWAs**
   - **Description**: This input represents the risk-weighted assets for equity risk. Equity risk is the risk of loss due to changes in the market price of equity positions.
   - **Relation to Equation**: Similar to credit RWAs, equity RWAs are included in the sum of all risk-weighted assets in the equation. It contributes to the term \((	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})\).

3. **Operational RWAs**
   - **Description**: This input represents the risk-weighted assets for operational risk. Operational risk is the risk of loss resulting from inadequate or failed internal processes, people, and systems, or from external events.
   - **Relation to Equation**: Operational RWAs are part of the total risk-weighted assets calculated in the equation, contributing to the term \((	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})\).

4. **Market RWAs**
   - **Description**: This input represents the risk-weighted assets for market risk. Market risk is the risk of losses in on- and off-balance-sheet positions arising from movements in market prices.
   - **Relation to Equation**: Market RWAs are included in the total risk-weighted assets in the equation, contributing to the term \((	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})\).

5. **CVA RWAs**
   - **Description**: This input represents the risk-weighted assets for credit valuation adjustment (CVA) risk. CVA risk refers to the risk of counterparty credit risk associated with derivative transactions.
   - **Relation to Equation**: CVA RWAs are part of the total risk-weighted assets in the equation, contributing to the term \((	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})\).

6. **Internal Model RWAs**
   - **Description**: This input represents the risk-weighted assets calculated using internal models. These models are developed by banks to estimate the potential risk and required capital.
   - **Relation to Equation**: Internal Model RWAs are compared against the output floor value in the equation to determine if they can be used or if the output floor value must be applied. The comparison ensures that internal model RWAs do not fall below 72.5% of the total RWAs calculated using standardized approaches.

7. **Internal Model Costs**
   - **Description**: This input represents the total costs incurred by the bank for implementing and maintaining internal models. These costs include development, validation, and operational expenses.
   - **Relation to Equation**: Internal Model Costs are used to evaluate whether the benefits of using internal models outweigh the costs. The cost-benefit analysis ensures that the bank only uses internal models if the benefit from using them is greater than the cost-benefit threshold.

## Equation Reference

The equation provided in the image for calculating the output floor is:

\(
	ext{Output Floor} = 72.5\% 	imes (	ext{Credit RWAs} + 	ext{Equity RWAs} + 	ext{Operational RWAs} + 	ext{Market RWAs} + 	ext{CVA RWAs})
\)

Each of the RWAs inputs contributes to the total sum of risk-weighted assets in this equation, determining the output floor value that sets a minimum bound on the risk-weighted assets for regulatory purposes.
