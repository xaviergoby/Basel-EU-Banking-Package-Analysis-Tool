import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")


class OutputFloorCalculator:
    def __init__(self, credit_rwas, equity_rwas, operational_rwas, market_rwas, cva_rwas, internal_model_rwas, internal_model_costs):
        """
        Initializes the OutputFloorCalculator with the risk-weighted assets and internal model costs.

        :param credit_rwas: Risk-weighted assets for credit risk
        :param equity_rwas: Risk-weighted assets for equity risk
        :param operational_rwas: Risk-weighted assets for operational risk
        :param market_rwas: Risk-weighted assets for market risk
        :param cva_rwas: Risk-weighted assets for credit valuation adjustment risk
        :param internal_model_rwas: Risk-weighted assets calculated using internal models
        :param internal_model_costs: Total costs incurred for implementing the internal model
        """
        self.credit_rwas = credit_rwas
        self.equity_rwas = equity_rwas
        self.operational_rwas = operational_rwas
        self.market_rwas = market_rwas
        self.cva_rwas = cva_rwas
        self.internal_model_rwas = internal_model_rwas
        self.internal_model_costs = internal_model_costs
        self.output_floor_percentage = 0.725  # 72.5%
        self.max_benefit_percentage = 0.275  # 27.5%

    def calculate_output_floor(self):
        """
        Calculates the output floor for the given risk-weighted assets.

        :return: Calculated output floor value
        """
        total_rwas = (self.credit_rwas + self.equity_rwas + self.operational_rwas +
                      self.market_rwas + self.cva_rwas)
        output_floor = self.output_floor_percentage * total_rwas
        return output_floor

    def determine_rwa_usage(self):
        """
        Determines whether the bank can use the internal model RWAs or must use the output floor value.

        :return: Tuple containing the chosen RWA value and a string indicating the source ('Internal Model' or 'Output Floor')
        """
        output_floor_value = self.calculate_output_floor()
        max_allowed_internal_model_rwas = (1 - self.max_benefit_percentage) * output_floor_value
        if self.internal_model_rwas >= max_allowed_internal_model_rwas:
            return self.internal_model_rwas, 'Internal Model'
        else:
            return output_floor_value, 'Output Floor'

    def evaluate_internal_model_costs(self):
        """
        Evaluates whether the total costs for implementing the internal model are worth it, based on the benefits.

        :return: Tuple containing a boolean indicating if the internal model is worth it, and a string explanation
        """
        output_floor_value = self.calculate_output_floor()
        benefit_from_internal_model = self.internal_model_rwas - output_floor_value
        cost_benefit_threshold = self.internal_model_costs / self.max_benefit_percentage

        if benefit_from_internal_model > cost_benefit_threshold:
            return True, 'The internal model is worth the cost.'
        else:
            return False, 'The internal model is not worth the cost. Stick to the standard model.'


def plot_comparison(standard_rwas, internal_model_rwas, output_floor):
    fig, ax = plt.subplots()
    labels = ['With standardised approach', 'With internal models']
    rwas = [standard_rwas, internal_model_rwas]
    output_floors = [standard_rwas, output_floor]

    bar_width = 0.35
    bar1 = ax.bar(labels, rwas, bar_width, label='RWAs', color='lightgreen')
    bar2 = ax.bar(labels, output_floors, bar_width, label='Output floor', color='brown', alpha=0.7)

    ax.set_xlabel('Approach', fontsize=14)
    ax.set_ylabel('RWAs', fontsize=14)
    ax.set_title('Standard Model vs Internal Model Trade-Off', fontsize=16)
    ax.legend(fontsize=12)

    for bar in bar1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom', fontsize=12)  # va: vertical alignment

    for bar in bar2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, int(yval), va='bottom', fontsize=12)  # va: vertical alignment

    st.pyplot(fig)


def interactive_plot_comparison(standard_rwas, internal_model_rwas, output_floor):
    data = {
        'Approach': ['With standardised approach', 'With internal models'],
        'RWAs': [standard_rwas, internal_model_rwas],
        'Output Floor': [standard_rwas, output_floor]
    }
    df = pd.DataFrame(data)
    df = df.melt('Approach', var_name='Type', value_name='Value')

    st.bar_chart(df, x='Approach', y='Value', color='Type', use_container_width=True)


# Streamlit app
st.title("Basel III Output Floor Calculator")

st.sidebar.header("Enter Risk-Weighted Assets (RWAs) and Costs")
credit_rwas = st.sidebar.number_input("Credit RWAs", min_value=0, value=400000000)
equity_rwas = st.sidebar.number_input("Equity RWAs", min_value=0, value=100000000)
operational_rwas = st.sidebar.number_input("Operational RWAs", min_value=0, value=50000000)
market_rwas = st.sidebar.number_input("Market RWAs", min_value=0, value=80000000)
cva_rwas = st.sidebar.number_input("CVA RWAs", min_value=0, value=20000000)
internal_model_rwas = st.sidebar.number_input("Internal Model RWAs", min_value=0, value=370000000)
internal_model_costs = st.sidebar.number_input("Internal Model Costs", min_value=0, value=5000000)

st.sidebar.subheader("Calculation Documentation")
st.sidebar.markdown("""
### Output Floor Calculation
The output floor is a key component of Basel III reforms aimed at ensuring banks maintain a minimum level of capital adequacy. It is calculated as:
\[
\text{Output Floor} = 72.5\% \times (\text{Credit RWAs} + \text{Equity RWAs} + \text{Operational RWAs} + \text{Market RWAs} + \text{CVA RWAs})
\]
This approach limits the benefit banks can derive from using internal models for calculating risk-weighted assets (RWAs).
""")

if st.sidebar.button("Calculate Output Floor"):
    calculator = OutputFloorCalculator(credit_rwas, equity_rwas, operational_rwas, market_rwas, cva_rwas, internal_model_rwas, internal_model_costs)
    output_floor_value = calculator.calculate_output_floor()
    chosen_rwa, source = calculator.determine_rwa_usage()
    is_worth_it, explanation = calculator.evaluate_internal_model_costs()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Results")
        st.write(f"Output Floor Value: {output_floor_value}")
        st.write(f"Chosen RWA Value: {chosen_rwa} (Source: {source})")
        st.write(f"Is Internal Model Worth It? {is_worth_it}: {explanation}")

        st.subheader("Calculation Documentation")
        st.markdown("""
        ### Determining RWA Usage
        Basel III requires banks to use the higher of their internal model RWAs or the output floor value. The max allowed internal model RWAs is calculated as:
        \[
        \text{Max Allowed Internal Model RWAs} = (1 - 27.5\%) \times \text{Output Floor}
        \]
        If the internal model RWAs are greater than or equal to this value, the bank can use the internal model RWAs. Otherwise, it must use the output floor value.
        """)

        st.markdown("""
        ### Evaluating Internal Model Costs
        To determine if the internal model costs are justified:
        \[
        \text{Benefit from Internal Model} = \text{Internal Model RWAs} - \text{Output Floor}
        \]
        \[
        \text{Cost Benefit Threshold} = \frac{\text{Internal Model Costs}}{27.5\%}
        \]
        If the benefit from using the internal model exceeds the cost benefit threshold, it is worth the cost. Otherwise, it is not.
        """)

        st.markdown("""
        ### Additional Information
        The output floor ensures that the variability of RWAs due to internal models is kept within acceptable limits, enhancing comparability and confidence in capital ratios. By constraining the benefits from internal models, Basel III aims to maintain a level playing field among banks and strengthen the overall financial system.
        """)

    with col2:
        st.subheader("Graphical Visualization")
        tab1, tab2 = st.tabs(["Static Visualization", "Interactive Visualization"])

        with tab1:
            st.write("### Static Visualization")
            plot_comparison(credit_rwas + equity_rwas + operational_rwas + market_rwas + cva_rwas, internal_model_rwas, output_floor_value)

        with tab2:
            st.write("### Interactive Visualization")
            interactive_plot_comparison(credit_rwas + equity_rwas + operational_rwas + market_rwas + cva_rwas, internal_model_rwas, output_floor_value)

# Increase the font size globally
st.markdown("""
    <style>
    .css-1d391kg, .css-1aumxhk, .css-1v3fvcr {
        font-size: 125% !important;
    }
    </style>
    """, unsafe_allow_html=True)
