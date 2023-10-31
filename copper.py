import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from streamlit_extras.mention import mention 
import pickle
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import re
import plotly.graph_objs as go
st.set_page_config(page_title='copper', layout='wide', page_icon="🪙")

st.write("""
<div style='text-align:right'>
    <h1 style='color:#B87333;'>🪙Industrial Copper Modeling</h1>
</div>
""", unsafe_allow_html=True)

def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#9AD8E1",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


with open("style1.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
#####################
# Navigation

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #16A2CB;">
  <a class="navbar-brand" href="https://www.linkedin.com/in/vengatesan2612/" target="_blank">Industrial Copper Modeling</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="/">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#predict-price">Price</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#predict-status">Status</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

st.write("The industrial copper market is dynamic and subject to various factors that influence its selling price. Accurately predicting the selling price of copper is crucial for manufacturers, traders, and stakeholders to make informed business decisions and plan their operations effectively. Additionally, categorizing the status of copper transactions helps in monitoring and streamlining the transaction lifecycle.")     
st.write("The goal of this project is to develop a machine learning solution that predicts the selling price of copper based on historical transaction data and classifies the status of each transaction. By leveraging features such as item date, quantity (in tons), customer information, country, item type, application, dimensions (thickness, width), and material/product references, the model aims to provide reliable price predictions and status classifications.")

col1,col2 = st.columns([8,2])
with col2 :
    st_lottie("https://lottie.host/7ea5bce6-95db-43aa-899b-35e8b4c41051/HsYZa8O49n.json",height=400)  

with col1:   
    data = {
    'Features': [
        "Quantity tons",
        "Customer",
        "Country",
        "Status",
        "Item type",
        "Application",
        "Thickness",
        "Width",
        "Product_ref",
        "Selling_price"
    ],
    'Detail': [
        "The amount of copper in tons associated with a specific transaction or item.",
        "The entity or organization purchasing the copper.",
        "The country associated with the customer or the location of the transaction.",
        "The current status of the transaction or item (e.g., pending, completed, in progress). Classification models can predict and categorize this status.",
        "The type or category of the copper item (e.g., raw copper, processed copper, copper alloys",
        "The intended use or application of the copper item (e.g., manufacturing, construction, electronics",
        "The thickness of the copper item, relevant for certain applications.",
        "The width of the copper item, relevant for specific industrial purposes.",
        "A reference or code related to the specific copper product.",
        "The price at which the copper was sold for a particular transaction. This is the target variable for prediction in the model."
    ]
}

# Create a DataFrame from the data
    df = pd.DataFrame(data)
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
# Create a Plotly table
    table = go.Figure(data=[go.Table(
    header=dict(values=["Features", "Detail"],line_color='darkslategray',
                fill_color=headerColor,align='center',font=dict(color='white', size=12)),
    cells=dict(values=[df['Features'], df['Detail']],line_color='darkslategray',font = dict(color = 'darkslategray', size = 10),
            fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor, rowEvenColor,rowOddColor, rowEvenColor,rowOddColor,rowEvenColor,rowOddColor,rowEvenColor,rowOddColor,rowEvenColor]*14],align='left'))
])

# Set the table layout
    table.update_layout(title="Below is a brief explanation of the Features  :")

# Streamlit
    st.plotly_chart(table,use_container_width=True)

st.markdown('''
<h2 style="color:#B87333; margin-bottom: 0;">Predict Price</h2>
<hr style="border: 1px solid #FFA500; background-color: #FFA500; margin-top: 0;">
''', unsafe_allow_html=True)
status_options = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised', 'Offered', 'Offerable']
item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
country_options = [28., 25., 30., 32., 38., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25., 67., 79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
product=['611112', '611728', '628112', '628117', '628377', '640400', '640405', '640665', 
            '611993', '929423819', '1282007633', '1332077137', '164141591', '164336407', 
            '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662', 
            '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738', 
            '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']

# Define the widgets for user input
with st.form("my_form"):
    col1,col2,col3=st.columns([5,2,5])
with col1:
    st.write(' ')
    status = st.selectbox("Status", status_options,key=1)
    quantity_tons = st.slider("Quantity Tons (Min: 611728, Max: 1722207579)", 611728.0, 1722207579.0, step=1.0)   
    country = st.selectbox("Country", sorted(country_options),key=3)
    width = st.slider("Width (Min: 1, Max: 2990)", 1.0, 2990.0, step=1.0)   
    product_ref = st.selectbox("Product Reference", product,key=5)
with col3:               
    st.write(' ')
    item_type = st.selectbox("Item Type", item_type_options,key=2)
    thickness = st.slider("Thickness (Min: 0.18, Max: 400)", 0.18, 400.0, step=0.01)
    application = st.selectbox("Application", sorted(application_options),key=4)
    customer = st.slider("Customer ID (Min: 12458, Max: 30408185)", 12458.0, 30408185.0, step=1.0)
    submit_button = st.form_submit_button(label="SELLING PRICE")

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #B87333;
            color: #f5e68c;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

flag = 0
pattern = "^(?:\d+|\d*\.\d+)$"

for i in [quantity_tons, thickness, width, customer]:
    if re.match(pattern, str(i)):
        pass
    else:
        flag = 1
        break

if submit_button and flag == 1:
    st.write("Please enter a valid number; spaces are not allowed.")

if submit_button and flag == 0:
            with open(r"Model/rmodel.pkl", 'rb') as file:
                loaded_model = pickle.load(file)
            with open(r'Model/rscaler.pkl', 'rb') as f:
                scaler_loaded = pickle.load(f)

            with open(r"Model/encr.pkl", 'rb') as f:
                t_loaded = pickle.load(f)

            with open(r"Model/renc.pkl", 'rb') as f:
                s_loaded = pickle.load(f)

            new_sample= np.array([[np.log(float(quantity_tons)),application,np.log(float(thickness)),float(width),country,float(customer),int(product_ref),item_type,status]])
            

            new_sample_ohe = t_loaded.transform(new_sample[:, [7]]).toarray()
            new_sample_be = s_loaded.transform(new_sample[:, [8]]).toarray()
            new_sample = np.concatenate((new_sample[:, [0,1,2, 3, 4, 5, 6,]], new_sample_ohe, new_sample_be), axis=1)
            new_sample1 = scaler_loaded.transform(new_sample)
            new_pred = loaded_model.predict(new_sample1)[0]
            rounded_pred = round(new_pred, 2)  # Round to 2 decimal placescol1,col2 = st.columns([9,1])
            col1,col2 = st.columns([9,1])
            with col1 :
             st.write(' ')
             st.write(' ')
             st.warning(f'Predicted selling price 🪙: 💲 {rounded_pred}')

            with col2:
                st.markdown(
                    f"""
                    <div class="coin">
                        <p style="font-weight: bold; color: brown;">${rounded_pred}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <style>
                    .coin {
                        width: 100px;
                        height: 100px;
                        background-color: #f9c834;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #fff;
                        box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.5);
                        background-image: url('https://th.bing.com/th/id/OIP.W1-HjtYRZPnfs4n_HO-rgwHaHR?pid=ImgDet&rs=1.png');
                        background-size: 100% 100%;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            
add_vertical_space(6)  
st.markdown('''
<h2 style="color:#B87333; margin-bottom: 0;">Predict Status</h2>
<hr style="border: 1px solid #FFA500; background-color: #FFA500; margin-top: 0;">
''', unsafe_allow_html=True) 
with st.form("my_form1"):
 col1,col2,col3=st.columns([5,1,5])
 with col1:
    ccountry = st.selectbox("Country", sorted(country_options),key=31)
    cquantity_tons = st.slider("Quantity Tons (Min: 611728, Max: 1722207579)", 611728.0, 1722207579.0, step=1.0)
    cwidth = st.slider("Enter width (Min:1, Max:2990)",1.0,2990.0,step=1.0)      
    cproduct_ref = st.selectbox("Product Reference", product,key=51)
    cselling = st.slider("Selling Price (Min:1, Max:100001015)",1.0,100001015.0,step=1.0) 
    
 with col3:    
    st.write(' ')
    
    citem_type = st.selectbox("Item Type", item_type_options,key=21)
    cthickness = st.slider("Enter thickness (Min:0.18 & Max:400)",0.18,400.0,step=1.0)
    capplication = st.selectbox("Application", sorted(application_options),key=41)  
    ccustomer = st.slider("customer ID (Min:12458, Max:30408185)",12458.0,30408185.0,step=1.0)
               
    csubmit_button = st.form_submit_button(label="CHECK STATUS")

 cflag = 0
pattern = r"^(?:\d+|\d*\.\d+)$"

# Convert the float values to strings before applying regex
cquantity_tons_str = str(cquantity_tons)
cthickness_str = str(cthickness)
cwidth_str = str(cwidth)
ccustomer_str = str(ccustomer)
cselling_str = str(cselling)

for k in [cquantity_tons_str, cthickness_str, cwidth_str, ccustomer_str, cselling_str]:
    if re.match(pattern, k):
        pass
    else:
        cflag = 1
        break

if csubmit_button and cflag == 1:
    if len(k) == 0:
        st.write("Please enter a valid number. Space is not allowed.")
    else:
        st.write("You have entered an invalid value: ", k)  
    
if csubmit_button and cflag==0:
 
    with open(r"Model/model_class.pkl", 'rb') as file:
        cloaded_model = pickle.load(file)

    with open(r'Model/scaler_class.pkl', 'rb') as f:
        cscaler_loaded = pickle.load(f)

    with open(r"Model/enc_class.pkl", 'rb') as f:
        ct_loaded = pickle.load(f)


    new_sample = np.array([[np.log(float(cquantity_tons)), np.log(float(cselling)), capplication, np.log(float(cthickness)),float(cwidth),ccountry,int(ccustomer),int(product_ref),citem_type]])
    new_sample_ohe = ct_loaded.transform(new_sample[:, [8]]).toarray()
    new_sample = np.concatenate((new_sample[:, [0,1,2, 3, 4, 5, 6,7]], new_sample_ohe), axis=1)
    new_sample = cscaler_loaded.transform(new_sample)
    new_pred = cloaded_model.predict(new_sample)
    col3,col4 = st.columns([9,1])
    with col3 : 
        st.write(' ')
        st.write(' ')
        if new_pred==1:
            st.success(f'Predicted Status : 👍 Won')
        else:
            st.warning(f'Predicted Status : 👎 Lost')
    with col4 :    
        st.markdown(
        f"""
        <div class="coin">
            <p style="font-weight: bold; color: brown;">{"Won" if new_pred == 1 else "Lost"}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
            """
            <style>
            .coin {
                width: 100px;
                height: 100px;
                background-color: #f9c834;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                color: #fff;
                box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.5);
                background-image: url('https://th.bing.com/th/id/OIP.W1-HjtYRZPnfs4n_HO-rgwHaHR?pid=ImgDet&rs=1.png');
                background-size: 100% 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
col4,col6 =st.columns([8,2])
with col6:
    st.write(' ')    
    add_vertical_space(3)
    mention(
        label="Vengatesan K",
        icon="streamlit",  # Some icons are available... like Streamlit!
        url="https://github.com/Vengatesan-K/Industrial-Copper-Modeling",
        )
                
#========================================== End =============================#
