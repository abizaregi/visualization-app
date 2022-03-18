import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Visualization with anotation", page_icon="💬", layout="centered"
)
st.title("💬 visualization with annotation")
source = pd.read_csv('indexData.csv')

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart_1(data):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    lines = (
        alt.Chart(data, title="Close Index Price")
        .mark_line()
        .encode(
            x="Date",
            y="Close",
            color="Index",
            # strokeDash="Index",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Date",
            y="Close",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("Close", title="Close"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart_2(data):
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    lines = (
        alt.Chart(data, title="Volume Index Price")
        .mark_line()
        .encode(
            x="Date",
            y="Volume",
            color="Index",
            # strokeDash="Index",
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Date",
            y="Volume",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("Volume", title="Volume"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()

st.write("Give more context to your visualization using annotations!")

source = pd.read_csv('example-app-time-series-annotation\indexData.csv')
source['Date'] = pd.to_datetime(source['Date'])
indexSelected = source.Index.unique()
index = st.multiselect('select index to display', indexSelected, indexSelected[:5])
source = source[source['Date'] >= '2019-01-01']
source = source[source.Index.isin(index)]
space(2)
chart = get_chart_1(source)
a, b = st.columns(2)
with a:
    date_annot = st.text_input('Insert date to annotate', '2020/01/01')
with b:
    event_annot = st.text_input('Insert event to annotate', 'insert event..')

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.selectbox("Choose a ticker", ('💬','⬇','👇','ℹ️'), 0)
with col2:
    ticker_dx = st.slider(
        "Horizontal offset", min_value=-100, max_value=30, step=1, value=5
    )
with col3:
    ticker_dy = st.slider(
        "Vertical offset", min_value=-100, max_value=30, step=1, value=-5
    )

space(2)

ANNOTATIONS = [
    (date_annot, event_annot)
]

annotations_df_1 = pd.DataFrame(ANNOTATIONS, columns=['Date', 'event'])
annotations_df_1.date = pd.to_datetime(annotations_df_1.Date)
annotations_df_1["y"] = 0
annotation_layer_1 = (
    alt.Chart(annotations_df_1)
    .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
    .encode(
        x="Date:T",
        y=alt.Y("y:Q"),
        tooltip=["event"],
    )
    .interactive()
)

st.altair_chart((chart + annotation_layer_1).interactive(), use_container_width=True)

st.write('-------------------------------------------------------------------------------------')

chart = get_chart_2(source)
a, b = st.columns(2)
with a:
    date_annot_1 = st.text_input('Insert date to annotate', '2020/01/02')
with b:
    event_annot_1 = st.text_input('Insert event to annotate', 'insert event...')

col1, col2, col3 = st.columns(3)
with col1:
    ticker_1 = st.selectbox("Choose a ticker", ('💬','⬇','👇','ℹ️'), 2)
with col2:
    ticker_dx_1 = st.slider(
        "Horizontal offset", min_value=-100, max_value=30, step=1, value=0
    )
with col3:
    ticker_dy_1 = st.slider(
        "Vertical offset", min_value=-100, max_value=30, step=1, value=-6
    )

space(2)

ANNOTATIONS = [
    (date_annot, event_annot)
]

annotations_df_2 = pd.DataFrame(ANNOTATIONS, columns=['Date', 'event'])
annotations_df_2.date = pd.to_datetime(annotations_df_2.Date)
annotations_df_2["y"] = 0
annotation_layer_2 = (
    alt.Chart(annotations_df_2)
    .mark_text(size=15, text=ticker_1, dx=ticker_dx_1, dy=ticker_dy_1, align="center")
    .encode(
        x="Date:T",
        y=alt.Y("y:Q"),
        tooltip=["event"],
    )
    .interactive()
)

st.altair_chart((chart + annotation_layer_2).interactive(), use_container_width=True)
