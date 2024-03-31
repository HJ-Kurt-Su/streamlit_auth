import streamlit as st 
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import main_app






def main():
    st.header("Page Purpose & Description")
    st.markdown("**Strain Calculator**: Calculate principal strain/strain rate for $$45^o$$ rosette gauge")

    with open('.\config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # authenticator.login()
    name, authentication_status, username = authenticator.login(location="main")

    if authentication_status:
        with st.sidebar.container():
            cols1,cols2 = st.columns(2)
            cols1.write('Welcome *%s*' % (name))
            with cols2.container():
                authenticator.logout('Logout', 'sidebar', key='unique_key')
        main_app.main()
        authenticator.logout()
        # st.write(f'Welcome *{st.session_state["name"]}*')
        # st.title('Some content')
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

    # st.markdown("**concate**: Concate Predict & Real Data")
    # st.markdown("**regression**: Regression tool with linear & taguchi method")
    # st.markdown("**predict**: Predict result with load trained model")

if __name__ == '__main__':

    st.title("Author & License:")

    st.markdown("**Kurt Su** (phononobserver@gmail.com)")

    # st.markdown("**This tool release under [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/) license**")

    st.markdown("               ")
    st.markdown("               ")

    
    main()