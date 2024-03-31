import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt
import numpy as np
import io
import plotly.graph_objects as go


#%% Sub Function

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


def convert_fig(fig):

    mybuff = io.StringIO()
   
    # fig_html = fig_pair.write_html(fig_file_name)
    fig.write_html(mybuff, include_plotlyjs='cdn')
    html_bytes = mybuff.getvalue().encode()

    return html_bytes

# %%

def backend_cal(df_cal, para_dict):

    df_prin = pd.DataFrame()

    start_time = df_cal[0][0]

    df_prin["Time"] = df_cal[0]-start_time
    time_unit = para_dict["time_unit"]
    strain_unit  = para_dict["strain_unit"]
    if time_unit == "millisecond":
        df_prin["Time"] = df_prin["Time"]/1000

    if strain_unit == "$\epsilon$":
        trans = 1000000
    else:
        trans = 1

    # Calculate principal max/min
    # i = 1

    color_sequence = ["#65BFA1", "#A4D6C1", "#D5EBE1", "#EBF5EC", "#00A0DF", "#81CDE4", "#BFD9E2"]
    color_sequence = px.colors.qualitative.Pastel
    template = "simple_white"


    rosette_num = 3
    corner_num = int(df_cal.shape[1]/3) + 1
    fig_sta = go.Figure()

    for i in range(1, corner_num):
        corn_name = "Conr_" + str(i)
        # ch_name
        ch1 = 1+(i-1)*rosette_num
        ch2 = 2+(i-1)*rosette_num
        ch3 = 3+(i-1)*rosette_num
        part_1 = (df_cal[ch1] + df_cal[ch3])/2
        part_2_1 = (df_cal[ch1] - df_cal[ch2])**2
        part_2_2 = (df_cal[ch2] - df_cal[ch3])**2
        part_2 = ((part_2_1 + part_2_2)/2)**0.5

        df_prin[corn_name+"_max"] = (part_1 + part_2) * trans
        df_prin[corn_name+"_min"] = (part_1 - part_2) * trans

        x_name = df_prin.columns[1+(i-1)*2]
        y_name = df_prin.columns[2+(i-1)*2]

        fig_sta.add_trace(go.Scatter(x=df_prin[x_name], y=df_prin[y_name], mode="markers", name=x_name))




    df_diff = df_prin.diff()
    time_diff = df_diff["Time"][1]
    df_rate = df_diff/time_diff
    df_rate["Time"] = df_prin["Time"]
    df_rate.fillna(0, inplace=True)
    # df_rate

    fig_rate = px.line(df_rate, x='Time', y=df_rate.columns,
                        color_discrete_sequence=color_sequence, template=template, 
                        )

    fig_prin = px.line(df_prin, x='Time', y=df_prin.columns,
                        color_discrete_sequence=color_sequence, template=template, 
                        )
        # fig_srs.update_yaxes(title_font_family="Arial")
    return df_prin, df_rate, fig_prin, fig_rate, fig_sta

def main():

    st.title('Rosette Strain Calculate Tool')

    st.markdown("               ")
    st.markdown("               ")

    uploaded = st.sidebar.file_uploader('#### 選擇您要上傳的 CSV 檔', type=["csv", "txt", "xlsx"])

    st.header('參數設定 (Parameter Setting)：')
    sk_row = st.number_input("Please Input Skip Rows", min_value=1, max_value=100, value=15)
    time_unit = st.radio(
        "**Select Time Unit Type:**",
        ["second", "millisecond"],
            # captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
        )

    strain_unit = st.radio(
        "**Select Strain Unit Type:**",
        ["$\mu$ $\epsilon$", "$\epsilon$"],
            # captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
        )
    
    para_dict = {"time_unit": time_unit, "strain_unit": strain_unit}
    
    if uploaded is not None:
        sub_name = uploaded.name.split(".")[1]
        if sub_name == "csv" or sub_name=="txt":

        # st.markdown(uploaded)
            df_raw = pd.read_csv(uploaded, skiprows=sk_row, sep="\s+|\t+", encoding="utf-8")
        elif sub_name == "xlsx":
            ch_type = st.radio(
                "**Select Channel In Sheet Type:**",
                ["All Channel In 1 Sheet", "1 Channel In 1 Sheet(SignalExpress)"],
            # captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
                )
            if ch_type == "1 Channel In 1 Sheet(SignalExpress)":

                xl = pd.ExcelFile(uploaded)
                sheet = xl.sheet_names
                # sk_row = 9
                df_raw = pd.DataFrame()
                df_raw["Time"] = pd.read_excel(uploaded, skiprows=sk_row, usecols="A")
                for i in sheet:
                    df_tmp = pd.read_excel(uploaded, sheet_name=i, skiprows=sk_row, usecols="B")
                    df_raw[i] = df_tmp
            elif ch_type == "All Channel In 1 Sheet":
                df_raw = pd.read_excel(uploaded, skiprows=sk_row)

        st.header('您所上傳的檔案內容：')

    # else:
    #     if input_method == "Ideal Wave Profile":
    #         st.header('Ideal Wave')
    #         df_accel = df_id_wv.copy()
    else:
        st.header('未上傳檔案，以下為 Demo：')
        uploaded_csv = "strain_trial.csv"
        df_raw = pd.read_csv(uploaded_csv, encoding="utf-8")

    # df_raw
        
    show_raw = st.checkbox("Show Raw Data")
    show_prin = st.checkbox("Show Principal Profile",value=True)
    show_rate = st.checkbox("Show Strain Rate Profile")
    show_state = st.checkbox("Show Strain State")

    if show_raw == True:
        df_raw
        fig_raw = px.line(df_raw, x=df_raw.columns[0], y=df_raw.columns,
                        # color_discrete_sequence=color_sequence, template=template, 
                        )
        st.subheader('Raw Data Profile：')
        st.plotly_chart(fig_raw, use_container_width=True)


    df_cal = df_raw.copy()
    df_cal.columns = range(0, df_raw.shape[1])
    date = str(dt.datetime.now()).split(" ")[0]

    df_prin, df_rate, fig_prin, fig_rate, fig_sta = backend_cal(df_cal, para_dict)


    if show_prin == True:
        st.subheader('Principal Strain Result')
        df_prin
        
        st.subheader('Principal Strain Summary：')
        prin_summary = df_prin.describe()
        prin_summary


        st.subheader('Principal Strain Profile：')
        st.plotly_chart(fig_prin, use_container_width=True)


        prin_result = convert_df(df_prin)
        prin_file_name_csv = date + "_principal.csv"

        st.download_button(label='Download principal result as CSV',  
                            data=prin_result, 
                            file_name=prin_file_name_csv,
                            mime='text/csv',
                            key="prin_csv")
    
    
    if show_rate == True:

        st.subheader('Principal Strain Rate：')
        df_rate

        st.subheader('Principal Strain Rate Profile：')
        st.plotly_chart(fig_rate, use_container_width=True)

        st.subheader('Principal Strain Rate Summary：')
        rate_summary = df_rate.describe()
        rate_summary

        prin_rate = convert_df(df_rate)
        rate_file_name_csv = date + "_strain_rate.csv"

        st.download_button(label='Download principal result as CSV',  
                            data=prin_rate, 
                            file_name=rate_file_name_csv,
                            mime='text/csv',
                            key="rate_csv")
    
    if show_state == True:
        st.subheader('Principal Strain State:')
        st.plotly_chart(fig_sta, use_container_width=True)


        fig_sta_name = date + "_strain_state.html"
        # fig_html = fig_pair.write_html(fig_file_name)
        sta_html = convert_fig(fig_sta)

        st.download_button(label="Download Strain State figure",
                            data=sta_html,
                            file_name=fig_sta_name,
                            mime='text/html',
                            key="sta_fig"
                            )



        

#%% Web App 頁面

if __name__ == '__main__':
    main()
# %%